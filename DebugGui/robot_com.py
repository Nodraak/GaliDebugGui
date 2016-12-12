#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from time import sleep, time
import re
import serial


class SerialRobot(object):
    def __init__(self, device, speed, log_file_out):
        try:
            self.fd = serial.Serial(device, speed, timeout=1)
            self.fd_out = open(log_file_out, 'w')
        except serial.serialutil.SerialException:
            print('[SerialRobot] Error opening serial port.')
            raise

    def should_read(self):
        return True

    def readline(self):
        try:
            ret = self.fd.readline().decode('ascii').strip()
            self.fd_out.write('%s\n' % ret)
            return ret
        except UnicodeDecodeError:
            print('[SerialRobot] received junk, ignoring (UnicodeDecodeError)')
            return None

    def quit(self):
        self.fd.close()
        self.fd_out.close()


class LoggedRobot(object):
    def __init__(self, filepath):
        self.fd = open(filepath)
        self.last_read_time = time()
        self.last_read_data = ''

    def should_read(self):
        # todo something smarter here
        return (time() - self.last_read_time) > 0.250

    def readline(self):
        ret = self.fd.readline().strip()
        if ret == '':
            self.last_read_time = time()
            self.last_read_data = ret
        return ret

    def quit(self):
        self.fd.close()


def parse_log_to_dic(input_logs):
    PATTERN = {
        "timer": {
            "loop": "",
            "match": "",
        },
        "MC/o_robot": {
            "speed": "",
            "angle": "",
            "x": "",
            "y": "",
        },
        "MC/i": {
            "r": "",
            "l": "",
        },
        "MC/t_pid": {
            "dist": "",
            "angle": "",
        },
        "MC/o_mot": {
            "lpwm": "",
            "rcurrent": "",
            "ldir": "",
            "lcurrent": "",
            "rdir": "",
            "rpwm": "",
        }
    }

    c = lambda pattern: re.compile(pattern, flags=re.MULTILINE)

    compiled_re = (
        c(r'^\[(?P<cat>timer)/match\] (?P<match>.+)$'),
        c(r'^\[(?P<cat>MC/i)\] (?P<l>.+) (?P<r>.+)$'),
        c(r'^\[(?P<cat>MC/t_pid)\] \(dist angle\) (?P<dist>.+) (?P<angle>.+)$'),
        c(r'^\[(?P<cat>MC/o_mot)\] \(dir pwm current\) (?P<ldir>.+) (?P<lpwm>.+) \((?P<lcurrent>.+) A\) \| (?P<rdir>.+) (?P<rpwm>.+) \((?P<rcurrent>.+) A\)$'),
        c(r'^\[(?P<cat>MC/o_robot)\] \(pos angle speed\) (?P<x>.+) (?P<y>.+) (?P<angle>.+) (?P<speed>.+)$'),
        c(r'^\[(?P<cat>timer)/loop\] (?P<loop>.+)$'),
    )

    matched = defaultdict(dict)

    for c in compiled_re:
        m = c.search(input_logs)
        if m:
            dic = m.groupdict()
            cat = dic.pop('cat')
            matched[cat].update(dic)

    try:
        check_hierarchy(matched, PATTERN)
    except AssertionError:
        return None

    return matched


def check_hierarchy(d1, d2):
    assert sorted(d1.keys()) == sorted(d2.keys())
    for k, v in d1.items():
        assert d1[k].__class__ == d2[k].__class__
        if isinstance(d1[k], dict):
            check_hierarchy(d1[k], d2[k])
        elif isinstance(d1[k], str):
            float(v)  # check that it can be casted to float
        else:
            raise ValueError('%s', d1[k].__class__)
