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


class Board(Gtk.DrawingArea):
    def __init__(self):
        super(Board, self).__init__()
        self.set_property('margin', 10)
        self.connect('draw', self.on_draw)

    def on_draw(self, canvas, cr):
        try:  # todo: this is ugly, please fix it
            x, y, angle = self.foo
        except AttributeError:
            x, y, angle = 0, 0, 0

        stuff_to_draw = [
            self.draw_board,
            self.draw_robot,
        ]

        win = canvas.get_window()
        # cr = win.cairo_create()
        w = win.get_width()
        h = win.get_height()

        cr.scale(0.2, 0.2)

        for callback in stuff_to_draw:
            cr.save()
            callback(cr, (w, h), (x, y, angle))
            cr.restore()

    def draw_board(self, cr, window_size, robot_pos):
        # clear
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, window_size[0], window_size[1])
        cr.fill()

        # draw board
        cr.set_source_rgb(0.9, 0.9, 0.9)
        cr.rectangle(0+50, 0+50, 2000, 3000)
        cr.fill()

        # draw grid
        size = 1
        cr.set_source_rgb(0.5, 0.5, 0.5)
        for x in range(0, 2000+1, 100):
            cr.rectangle(x+50, 0+50, size, 3000)
        for y in range(0, 3000+1, 100):
            cr.rectangle(0+50, y+50, 2000, size)
        cr.fill()
        cr.set_source_rgb(0, 0, 0)
        for x in range(0, 2000+1, 1000):
            cr.rectangle(x+50, 0+50, size, 3000)
        for y in range(0, 3000+1, 1000):
            cr.rectangle(0+50, y+50, 2000, size)
        cr.fill()


    def draw_robot(self, cr, window_size, robot_pos):
        x, y, angle = robot_pos
        robot_size = (400, 300)

        cr.set_source_rgb(0.5, 0.5, 1)
        cr.translate(x+50+robot_size[0]/2+100, -y+50+robot_size[1]/2+500)
        cr.rotate(-angle*math.pi/180 + math.pi/2)
        cr.rectangle(-robot_size[0]/2, -robot_size[1]/2, robot_size[0], robot_size[1])
        cr.fill()


class MapView(Gtk.Grid):
    def __init__(self):
        super(MapView, self).__init__()

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.canvas = Board()
        self.attach(self.canvas, 0, 0, 3, 1)

        infos = Gtk.VBox()
        self.attach(infos, 3, 0, 1, 1)

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
        # board

        self.canvas.foo = [float(f) for f in (dic['MC/o_robot']['x'], dic['MC/o_robot']['y'], dic['MC/o_robot']['angle'])]
        self.canvas.queue_draw()

        # infos

        self.labels['X']['Timer'].set_text('%s' % dic['timer']['match'])

        self.labels['Phys']['Pos'].set_text('%s %s' % (dic['MC/o_robot']['x'], dic['MC/o_robot']['y']))
        self.labels['Phys']['Angle'].set_text('%s' % dic['MC/o_robot']['angle'])
        self.labels['Phys']['Speed'].set_text('%s' % dic['MC/o_robot']['speed'])

        self.labels['MC']['Encs'].set_text('%s %s' % (dic['MC/i']['l'], dic['MC/i']['r']))
        self.labels['MC']['PID'].set_text('%s %s' % (dic['MC/t_pid']['dist'], dic['MC/t_pid']['angle']))


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
