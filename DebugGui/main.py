#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import select

from gi.repository import Gtk, GObject

from views import MapView, LogsView
from robot_com import SerialRobot, LoggedRobot, parse_log_to_dic

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
        """
            This function is called every X ms thanks to `GObject.timeout_add`.
            It read the robot debug log if needed (ie. without blocking) line by
            line, and when all information is gathered from a given robot main
            handling loop, this parse the data and update the gui.
        """

        while True:
            # read serial (serial2logs)

            ready_for_read, _, _ = select.select([self.robot.fd], [], [], 0)

            if len(ready_for_read) == 0:
                print('nothing to read, breaking')
                break

            line = self.robot.readline()
            if line != None:

                if line != '':
                    self.logs.append(line)
                    self.tmp_logs.append(line)
                else:
                    # parse logs (logs2data)

                    new_logs = '\n'.join(self.tmp_logs)
                    new_dic = parse_log_to_dic(new_logs)
                    self.tmp_logs = []

                    if new_dic:
                        self.data.append(new_dic)

                        # update gui (data2gui)
                        self.main_window.tabs['Map'].update_gui(new_dic)
                        self.main_window.tabs['Logs'].update_gui(new_logs)

                        print('updated gui')

                    break  # prevent the gui from becomming unresponsive

        return True  # call this function again


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()

        handlers = {
            'destroy': self.quit,
            'delete-event': self.quit,
        }
        self.tabs = OrderedDict((
            ('Map', MapView()),
            ('Logs', LogsView()),
        ))

        self.set_title('Gali debug')
        self.set_default_size(800, 600)
        self.set_border_width(10)
        for k, v in handlers.items():
            self.connect(k, v)

        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        for tab_title, tab_widget in self.tabs.items():
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
