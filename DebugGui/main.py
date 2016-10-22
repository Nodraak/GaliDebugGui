#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import select

from gi.repository import Gtk, GObject

from views import MapView, LogsView
from robot_com import SerialRobot, LoggedRobot

"""
Tabs:
    map (drawing area) + basic info
    infos
    logs (scrolling text + text edit)
    plots (matplolib / pyplot ?)

infos:
    Phys:
        pos, angle, speed
    MC:
        encs, motors (dir, pwm, ... consumption ?), pid
        orders
    IO:
        capteurs (sharp)
        actionneurs (ax12, servos, pompe)

"""

SERIAL_DEVICE = '/dev/ttyUSB0'
SERIAL_SPEED = 115200
LOG_FILE = '../Deoxys/log2.txt'


class App(object):
    def __init__(self):
        self.logs = []
        self.tmp_logs = []
        self.data = []

        # self.robot = SerialRobot(SERIAL_DEVICE, SERIAL_SPEED)
        self.robot = LoggedRobot(LOG_FILE)

        self.main_window = MainWindow()

        GObject.threads_init()
        GObject.timeout_add(1000./20, self.read_serial_and_update_gui)

        self.main_window.show_all()

    def run(self):
        self.main_window.run()

    def quit(self):
        self.robot.quit()

    def read_serial_and_update_gui(self):

        def parse(input_logs):
            return {'pos': 42}

        while True:
            # read serial (serial2logs)

            ready_for_read, _, _ = select.select([self.robot.fd], [], [], 0)

            if len(ready_for_read) == 0:
                break

            line = self.robot.readline()
            if line != None:

                if line != '':
                    self.logs.append(line)
                    self.tmp_logs.append(line)
                else:
                    # parse logs (logs2data)

                    self.data.append(parse(self.tmp_logs))
                    self.tmp_logs = []

                    # update gui (data2gui)
                    print('update gui with', self.data[-1])

                    break  # prevent the gui from becomming unresponsive

        return True  # call this function again


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()

        handlers = {
            'destroy': self.quit,
            'delete-event': self.quit,
        }
        tabs = (
            ('Map', MapView()),
            ('Logs', LogsView()),
        )

        self.set_title('Gali debug')
        self.set_default_size(800, 600)
        self.set_border_width(10)
        for k, v in handlers.items():
            self.connect(k, v)

        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        for tab_title, tab_widget in tabs:
            self.notebook.append_page(tab_widget, Gtk.Label(tab_title))
        self.add(self.notebook)

    def quit(self, *args):
        Gtk.main_quit()

    def run(self):
        Gtk.main()


def main():
    app = App()
    app.run()
    app.quit()


if __name__ == '__main__':
    main()
