#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


"""
def parse_serial_data(line):
    # m = re.match(r'^\[in/encs\] lr:( +-?\d+)( +-?\d+) \| avg:( +-?\d+) ticks( +-?\d+) mm$', line)
    # if m:
    #     return dict(zip(['enc_l_val', 'enc_r_val', 'input_dist', 'input_dist_mm'], m.groups()))

    # m = re.match(r'^\[out/motors\] dist:( +-?[\d.]+) raw( +-?[\d.]+) pwm \| angle:( +-?[\d.]+)$', line)
    # if m:
    #     return dict(zip(['output_dist_raw', 'output_dist_pwm', 'output_angle'], m.groups()))

    m = re.match(r'^\[MC/in\] (\d+) (\d+)$', line)
    if m:
        return dict(zip(['in_l', 'in_r'], m.groups()))
    m = re.match(r'^\[MC/o_robot\] (pos angle speed) (-?\d+) (-?\d+) (-?\d+) (-?\d+)$', line)
    if m:
        return dict(zip(['pos_x', 'pos_y', 'angle', 'speed'], m.groups()))

    return {}

"""
