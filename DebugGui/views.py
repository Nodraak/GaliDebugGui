#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import math

from gi.repository import Gtk, Gdk


class MyLabel(Gtk.Label):
    def __init__(self, *args, **kwargs):
        super(MyLabel, self).__init__(*args)
        for k, v in kwargs.items():
            getattr(self, k)(v)


class MapView(Gtk.Grid):
    def __init__(self):
        super(MapView, self).__init__()

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.canvas = Gtk.DrawingArea()
        self.canvas.set_property('margin', 10)
        self.attach(self.canvas, 0, 0, 1, 1)

        infos = Gtk.VBox()
        self.attach(infos, 1, 0, 1, 1)

        LABELS = OrderedDict((
            ('X', ('Timer', )),
            ('Phys', ('Pos', 'Angle', 'Speed')),
            ('MC', ('Encs', 'Motors', 'PID')),
            ('I/O', ('sensors', 'Act')),
        ))

        self.labels = {}
        for title, children in LABELS.items():
            label = MyLabel(set_markup='<b>%s:</b>' % title, set_halign=Gtk.Align.START)
            infos.pack_start(label, True, True, 0)

            for item in children:
                label = MyLabel('-', set_selectable=True)

                if title not in self.labels:
                    self.labels[title] = {}
                self.labels[title][item] = label

                line = Gtk.HBox()
                line.pack_start(MyLabel('%s:' % item, set_halign=Gtk.Align.START), True, True, 0)
                line.pack_start(label, True, True, 0)
                infos.pack_start(line, True, True, 0)

            infos.pack_start(Gtk.HSeparator(), True, True, 0)

    def update_gui(self, dic):
        self.labels['X']['Timer'].set_text(dic['timer/match'][0])

        self.labels['Phys']['Pos'].set_text('%s %s' % (dic['MC/o_robot'][0], dic['MC/o_robot'][1]))
        self.labels['Phys']['Angle'].set_text(dic['MC/o_robot'][2])
        self.labels['Phys']['Speed'].set_text(dic['MC/o_robot'][3])

        self.labels['MC']['Encs'].set_text('%s %s' % (dic['MC/i'][0], dic['MC/i'][1]))
        self.labels['MC']['PID'].set_text('%s %s' % (dic['MC/t_pid'][0], dic['MC/t_pid'][1]))

        self.draw_canvas(dic['MC/o_robot'][0], dic['MC/o_robot'][1], dic['MC/o_robot'][2])

    def draw_canvas(self, x, y, angle):
        win = self.canvas.get_window()
        cr = win.cairo_create()
        w = win.get_width()
        h = win.get_height()

        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        cr.set_source_rgb(0.9, 0.9, 0.9)
        cr.rectangle(0+50, 0+50, 200, 300)
        cr.fill()

        cr.set_source_rgb(0.5, 0.5, 1)
        cr.rotate(float(angle)*math.pi/180)
        cr.rectangle(float(x)+50, float(y)+50, 50, 50)
        cr.fill()


class LogsView(Gtk.Grid):
    def __init__(self):
        super(LogsView, self).__init__()

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.tb = Gtk.TextBuffer()
        self.tb.set_text('-')

        logs = Gtk.TextView()
        logs.set_buffer(self.tb)
        logs.set_editable(False)
        # logs.set_monospace(True)
        logs.set_left_margin(10)
        # logs.set_bottom_margin(10)
        logs.set_property('margin', 10)
        logs.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0.9, 0.9, 0.9, 1.0))

        self.sw = Gtk.ScrolledWindow()
        self.sw.add(logs)
        self.attach(self.sw, 0, 0, 1, 9)

        cmd = Gtk.Entry()
        # cmd.set_top_margin(10)
        cmd.set_property('margin', 10)
        self.attach(cmd, 0, 9, 1, 1)

    def update_gui(self, logs):
        self.tb.insert(self.tb.get_end_iter(), '\n\n'+logs)

        adj = self.sw.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
