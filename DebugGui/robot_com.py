#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import re
import serial


class SerialRobot(object):
    def __init__(self, device, speed):
        try:
            self.fd = serial.Serial(device, speed, timeout=1)
        except serial.serialutil.SerialException:
            print('[SerialRobot] Error opening serial port.')
            raise

    def readline(self):
        try:
            return self.fd.readline().decode('ascii').strip()
        except UnicodeDecodeError:
            print('[SerialRobot] received junk, ignoring (UnicodeDecodeError)')
            return None

    def quit(self):
        self.fd.close()


class LoggedRobot(object):
    def __init__(self, filepath):
        self.fd = open(filepath)

    def readline(self):
        return self.fd.readline().strip()

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
    for k in d1.keys():
        assert d1[k].__class__ == d2[k].__class__
        if isinstance(d1[k], dict):
            check_hierarchy(d1[k], d2[k])
