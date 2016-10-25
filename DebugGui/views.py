#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk, GObject


class MapView(Gtk.Grid):
    def __init__(self):
        super(Gtk.Grid, self).__init__()

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        button_1 = Gtk.Button(label='button 1')
        self.attach(button_1, 0, 0, 1, 1)

        infos = Gtk.VBox()
        self.attach(infos, 1, 0, 1, 1)

        self.labels = (
            (Gtk.Label('X'), (
                Gtk.Label('Timer'),
            )),
            (Gtk.Label('Phys'), (
                Gtk.Label('Pos'),
                Gtk.Label('Angle'),
                Gtk.Label('Speed'),
            )),
            (Gtk.Label('MC'), (
                Gtk.Label('Encs'),
                Gtk.Label('Motors (dir, pwm, ... consumption ?)'),
                Gtk.Label('PID'),
            )),
            (Gtk.Label('I/O'), (
                Gtk.Label('Sensors (sharps)'),
                Gtk.Label('Actionneurs (ax12, servo, pompe'),
            )),
            (Gtk.Label('Send order'), (
                Gtk.Label('Dist'),
                Gtk.Label('Angle'),
                Gtk.Label('Pos'),
            )),
        )

        for i, (title, childs) in enumerate(self.labels):
            infos.pack_start(title, True, True, 0)

            tmp = Gtk.VBox()
            for j, child in enumerate(childs):
                tmp.pack_start(child, True, True, 0)
            infos.pack_start(tmp, True, True, 5)
            infos.pack_start(Gtk.HSeparator(), True, True, 0)

    def update_gui(self, dic):
        label_timer = self.labels[0][1][0]
        label_timer.set_text('Timer: %s' % dic['timer/match'])


class LogsView(Gtk.Grid):
    def __init__(self):
        super(Gtk.Grid, self).__init__()

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        logs = Gtk.TextView()
        logs.set_editable(False)
        # logs.set_monospace(True)
        tb = Gtk.TextBuffer()
        tb.set_text('hello')
        logs.set_buffer(tb)
        logs.set_left_margin(10)
        # logs.set_bottom_margin(10)
        logs.set_property('margin', 10)
        logs.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0.9, 0.9, 0.9, 1.0))
        self.attach(logs, 0, 0, 1, 9)

        cmd = Gtk.Entry()
        # cmd.set_top_margin(10)
        cmd.set_property('margin', 10)
        self.attach(cmd, 0, 9, 1, 1)

    def update_gui(self, dic):
        pass  # todo
