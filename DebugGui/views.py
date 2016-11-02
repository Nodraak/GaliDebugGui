#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime
import math

from gi.repository import Gtk, Gdk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
import cairo


class MyLabel(Gtk.Label):
    def __init__(self, *args, **kwargs):
        super(MyLabel, self).__init__(*args)
        for k, v in kwargs.items():
            getattr(self, k)(v)


class MyGrid(Gtk.Grid):
    def __init__(self):
        super(MyGrid, self).__init__()

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        self.set_row_spacing(5)
        self.set_column_spacing(5)


class Board(Gtk.DrawingArea):
    COLORS = {
        'team1': (1, 1, 0.5),
        'team2': (0.5, 0.5, 1),
        'me': (0.3, 0.6, 0.3),

        'grid_sub': (0.7, 0.7, 0.7),
        'grid_main': (0.5, 0.5, 0.5),

        'board_bg': (0.9, 0.9, 0.9),
        'board_edge': (0.5, 0.5, 0.5),
        'elem_bg': (0.8, 0.8, 0.8),
        'elem_edge': (0.5, 0.5, 0.5),
    }
    ROBOT_SIZE = (300, 240)

    def __init__(self):
        super(Board, self).__init__()
        self.set_property('margin', 10)
        self.connect('draw', self.on_draw)

        self.eceborg = cairo.ImageSurface.create_from_png('Eceborg.png')

    def on_draw(self, canvas, cr):
        try:  # todo: this is ugly, please fix it
            x, y, angle = self.foo
        except AttributeError:
            x, y, angle = 0, 0, 0

        stuff_to_draw = [
            self.draw_board_static,
            self.draw_board_elem,
            self.draw_robot,
        ]

        win = canvas.get_window()
        # cr = win.cairo_create()
        w = win.get_width()
        h = win.get_height()

        # clear
        cr.set_source_rgb(0.95, 0.95, 0.95)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        cr.scale(0.2, 0.2)
        cr.translate(50, 50)

        cr.set_source_rgb(*self.COLORS['board_edge'])
        cr.rectangle(-20, -20, 2000+2*20, 3000+2*20)
        cr.fill()

        for callback in stuff_to_draw:
            cr.save()
            callback(cr, (x, y, angle))
            cr.restore()

    def draw_board_static(self, cr, robot_pos):
        # draw bg
        cr.set_source_rgb(*self.COLORS['board_bg'])
        cr.rectangle(0, 0, 2000, 3000)
        cr.fill()

        # draw grid
        size = 1
        cr.set_source_rgb(*self.COLORS['grid_sub'])
        for x in range(0, 2000+1, 100):
            cr.rectangle(x, 0, size, 3000)
        for y in range(0, 3000+1, 100):
            cr.rectangle(0, y, 2000, size)
        cr.fill()
        cr.set_source_rgb(*self.COLORS['grid_main'])
        for x in range(0, 2000+1, 1000):
            cr.rectangle(x, 0, size, 3000)
        for y in range(0, 3000+1, 1000):
            cr.rectangle(0, y, 2000, size)
        cr.fill()

        # starting points

        cr.set_source_rgb(*self.COLORS['team1'])
        cr.rectangle(0, 0, 360, 360)
        cr.rectangle(0, 360+350, 360, 360)
        cr.fill()

        cr.set_source_rgb(*self.COLORS['team2'])
        cr.rectangle(0, 3000-(2*360+350), 360, 360)
        cr.rectangle(0, 3000-360, 360, 360)
        cr.fill()

        cr.set_source_rgb(*self.COLORS['elem_edge'])
        cr.rectangle(360, 0, 22, 360+350)
        cr.rectangle(360, 3000-(360+350), 22, 360+350)
        cr.fill()

        # white balls

        cr.set_source_rgb(*self.COLORS['elem_edge'])

        cr.arc(540, 650, 170/2+30, 0, 2*math.pi)
        cr.arc(540, 2350, 170/2+30, 0, 2*math.pi)

        cr.move_to(2000, 0)
        cr.arc(2000, 0, 510+30, math.pi/2, -math.pi)
        cr.line_to(2000, 0)
        cr.move_to(2000, 3000)
        cr.arc(2000, 3000, 510+30, math.pi, 3*math.pi/2)
        cr.line_to(2000, 3000)

        cr.move_to(1870, 1070)
        cr.arc(1870, 1070, 170/2+30, 0, 2*math.pi)
        cr.move_to(1870, 1930)
        cr.arc(1870, 1930, 170/2+30, 0, 2*math.pi)

        cr.fill()


        cr.set_source_rgb(*self.COLORS['elem_bg'])

        cr.arc(540, 650, 170/2, 0, 2*math.pi)
        cr.arc(540, 2350, 170/2, 0, 2*math.pi)

        cr.move_to(2000, 0)
        cr.arc(2000, 0, 510, math.pi/2, -math.pi)
        cr.line_to(2000, 0)
        cr.move_to(2000, 3000)
        cr.arc(2000, 3000, 510, math.pi, 3*math.pi/2)
        cr.line_to(2000, 3000)

        cr.move_to(1870, 1070)
        cr.arc(1870, 1070, 170/2, 0, 2*math.pi)
        cr.move_to(1870, 1930)
        cr.arc(1870, 1930, 170/2, 0, 2*math.pi)

        cr.fill()

        # cylinders

        cr.set_source_rgb(*self.COLORS['elem_edge'])
        cr.rectangle(700-22, 0, 450+2*22, 80+28)
        cr.rectangle(700-22, 3000-(80+28), 450+2*22, 80+28)

        cr.fill()

        cr.set_source_rgb(*self.COLORS['elem_bg'])
        cr.rectangle(700, 0, 450, 80)
        cr.rectangle(700, 3000-80, 450, 80)

        cr.fill()

        cr.set_source_rgb(*self.COLORS['elem_edge'])
        cr.save()
        cr.translate(2000, 1500)
        cr.arc(0, 0, 200+10, math.pi/2, -math.pi/2)
        cr.rotate(-math.pi/4)
        cr.rectangle(-600-200, -(80+2*28)/2, 600, (80+2*28))
        cr.rotate(math.pi/4)
        cr.rectangle(-600-200, -(80+2*28)/2, 600, (80+2*28))
        cr.rotate(math.pi/4)
        cr.rectangle(-600-200, -(80+2*28)/2, 600, (80+2*28))
        cr.fill()
        cr.restore()

        cr.set_source_rgb(*self.COLORS['elem_bg'])
        cr.save()
        cr.translate(2000, 1500)
        cr.rotate(-math.pi/4)
        cr.rectangle(-600-200, -80/2, 600, 80)
        cr.rotate(math.pi/4)
        cr.rectangle(-600-200, -80/2, 600, 80)
        cr.rotate(math.pi/4)
        cr.rectangle(-600-200, -80/2, 600, 80)
        cr.fill()
        cr.restore()

        # rockets

        cr.set_source_rgb(*self.COLORS['elem_edge'])

        cr.arc(1350, 80/2, 80/2, 0, 2*math.pi)
        cr.arc(1350, 3000-80/2, 80/2, 0, 2*math.pi)
        cr.move_to(0, 0)
        cr.arc(80/2, 1150, 80/2, 0, 2*math.pi)
        cr.move_to(0, 0)
        cr.arc(80/2, 1850, 80/2, 0, 2*math.pi)

        cr.fill()

    def draw_board_elem(self, cr, robot_pos):
        cr.set_source_rgb(*self.COLORS['team1'])

        cr.arc(1350, 80/2, 76/2, 0, 2*math.pi)
        cr.arc(80/2, 1150, 76/2, 0, 2*math.pi)
        cr.fill()
        cr.arc(1850-80/2, 800-80/2, 76/2, 0, 2*math.pi)

        cr.fill()


        cr.set_source_rgb(*self.COLORS['team2'])

        cr.arc(1350, 3000-80/2, 76/2, 0, 2*math.pi)
        cr.arc(80/2, 1850, 76/2, 0, 2*math.pi)
        cr.fill()
        cr.arc(1850-80/2, 2200-80/2, 76/2, 0, 2*math.pi)

        cr.fill()

    def draw_robot(self, cr, robot_pos):
        x, y, angle = robot_pos

        cr.translate(x+self.ROBOT_SIZE[0]/2+0, -y+self.ROBOT_SIZE[1]/2+750)

        cr.save()

        cr.set_source_rgb(*self.COLORS['me'])
        cr.rotate(-angle*math.pi/180 + math.pi/2)
        cr.rectangle(-self.ROBOT_SIZE[0]/2, -self.ROBOT_SIZE[1]/2, self.ROBOT_SIZE[0], self.ROBOT_SIZE[1])
        cr.fill()
        cr.restore()

        cr.scale(2, 2)
        cr.set_source_surface(self.eceborg, -74/2, -74/2)
        cr.paint()
        cr.restore()


class MapView(MyGrid):
    def __init__(self):
        super(MapView, self).__init__()

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

        try:
            self.canvas.foo = [float(f) for f in (dic['MC/o_robot']['x'], dic['MC/o_robot']['y'], dic['MC/o_robot']['angle'])]
        except ValueError:
            self.canvas.foo = 0, 0, 0
        self.canvas.queue_draw()

        # infos

        self.labels['X']['Timer'].set_text('%s' % dic['timer']['match'])

        self.labels['Phys']['Pos'].set_text('%s %s' % (dic['MC/o_robot']['x'], dic['MC/o_robot']['y']))
        self.labels['Phys']['Angle'].set_text('%s' % dic['MC/o_robot']['angle'])
        self.labels['Phys']['Speed'].set_text('%s' % dic['MC/o_robot']['speed'])

        self.labels['MC']['Encs'].set_text('%s %s' % (dic['MC/i']['l'], dic['MC/i']['r']))
        self.labels['MC']['PID'].set_text('%s %s' % (dic['MC/t_pid']['dist'], dic['MC/t_pid']['angle']))


class LogsView(MyGrid):
    def __init__(self):
        super(LogsView, self).__init__()

        # todo bool autoscroll

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


class PlotsView(MyGrid):
    def __init__(self):
        super(PlotsView, self).__init__()

        fig = plt.figure()
        self.canvas = FigureCanvas(fig)
        self.xs = []
        self.plots = [
            ([], fig.add_subplot(2, 2, 1)),
            ([], fig.add_subplot(2, 2, 2)),
            ([], fig.add_subplot(2, 2, 3)),
            ([], fig.add_subplot(2, 2, 4)),
        ]

        self.add(self.canvas)

        self.last_draw = datetime.utcnow()

    def update_gui(self, dic):
        self.xs.append(dic['timer']['match'])
        self.plots[0][0].append(dic['MC/o_robot']['angle'])
        self.plots[1][0].append(dic['MC/o_robot']['x'])
        self.plots[2][0].append(dic['MC/o_robot']['y'])
        self.plots[3][0].append(dic['MC/o_robot']['speed'])

        if (datetime.utcnow()-self.last_draw).total_seconds() > 0.500:
            for ys, plot in self.plots:
                plot.cla()
                plot.plot(self.xs, ys)

            self.canvas.draw()
            self.last_draw = datetime.utcnow()
