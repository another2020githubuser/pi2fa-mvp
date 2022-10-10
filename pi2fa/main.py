import pi2fa_logging
from pi2fa.ui.gtk.application import Application

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio

def main():
    app = Application("pi.pi2fa.com", Gio.ApplicationFlags.FLAGS_NONE)
    app.run()

if __name__ == "__main__":
     main()
    