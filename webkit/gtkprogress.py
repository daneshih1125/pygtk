#!/usr/bin/env python3
from gi.repository import Gtk, WebKit
import os, re

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

class WebWindow(Gtk.Window):

    def __init__(self, html="", tpl={}):
        Gtk.Window.__init__(self, title='Progress bar')
        self.view = WebKit.WebView()
        self.add(self.view)
        settings = self.view.get_settings()
        settings.set_property('enable-default-context-menu', False)
        self.view.set_settings(settings)
        self.progress = 0
        if html:
            self.load_html(html, tpl)

    def load_html(self, html, tpl):
        fd = open(html, "r")
        self.tmp_page = fd.read()
        fd.close()
        for key, value in tpl.items():
            output_page = self.tmp_page.replace("{%s}" % key, value)
        self.view.load_html_string(output_page, ROOT_DIR + '/html/')

    def dispatch(self,view, frame, req, data=None):
        uri = req.get_uri()
        if uri.find("://") > 0:
            scheme, path = uri.split("://", 1)
        else:
            return False

        if scheme == 'file':
            return False
        elif scheme == 'admin' and path == "progress":
            self.progress += 1
            output_page = self.tmp_page.replace("{progress}", "%d" % self.progress)
            win.view.load_html_string(output_page, ROOT_DIR + '/html/')
        return True

if __name__ == '__main__':
    tpl = { "progress" : "0" }
    html = ROOT_DIR + "/html/progress.html"
    win = WebWindow(html, tpl)
    win.set_default_size(800, 600)
    win.set_position(Gtk.WindowPosition.CENTER)
    win.connect("delete-event", Gtk.main_quit)
    win.view.connect("navigation-requested", win.dispatch)
    win.show_all()
    Gtk.main()
