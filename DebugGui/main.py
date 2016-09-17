#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import Gdk


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


class App(Gtk.Window):
    def __init__(self, tabs):
        super(App, self).__init__()

        # gtk.gdk.threads_init()

        self.set_title('Gali debug')
        self.set_default_size(800, 600)
        for k, v in {
            'destroy': self.app_quit,
            'delete-event': self.app_quit,
        }.items():
            self.connect(k, v)
        self.set_border_width(10)

        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        self.notebook.connect("switch-page", self.page_changed)

        for tab_title, tab_widget in tabs:
            self.notebook.append_page(tab_widget, Gtk.Label(tab_title))

        self.add(self.notebook)

    def app_quit(self, *args):
        Gtk.main_quit()

    def main(self):
        Gtk.main()

    def page_changed(self, notebook, page, i):
        return
        tab_child = notebook.get_nth_page(i)
        tab_label = notebook.get_tab_label(tab_child)
        print(tab_label.get_text())


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

        labels = (
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

        for i, (title, childs) in enumerate(labels):
            infos.pack_start(title, True, True, 0)

            tmp = Gtk.VBox()
            for j, child in enumerate(childs):
                tmp.pack_start(child, True, True, 0)
            infos.pack_start(tmp, True, True, 5)
            infos.pack_start(Gtk.HSeparator(), True, True, 0)


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


def main():
    app = App((
        ('Map', MapView()),
        ('Logs', LogsView()),
    ))
    app.show_all()
    app.main()


if __name__ == '__main__':
    main()
