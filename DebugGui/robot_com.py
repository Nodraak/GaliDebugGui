#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    c = lambda pattern: re.compile(pattern, flags=re.MULTILINE)

    compiled_re = (
        c(r'^\[(timer/match)\] (.+)$'),
        c(r'^\[(MC/i)\] (.+) (.+)$'),
        c(r'^\[(MC/t_pid)\] \(dist angle\) (.+) (.+)$'),
        c(r'^\[(MC/o_mot)\] \(dir pwm current\) (.+) (.+) \((.+) A\) \| (.+) (.+) \((.+) A\)$'),
        c(r'^\[(MC/o_robot)\] \(pos angle speed\) (.+) (.+) (.+) (.+)$'),
        c(r'^\[(timer/loop)\] (.+)$'),
    )

    matched = {}

    for c in compiled_re:
        m = c.search(input_logs)
        if m:
            g = m.groups()
            matched[g[0]] = g[1:]

    return matched
