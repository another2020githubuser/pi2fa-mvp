'''Stores Gtk.Application required state'''

import pi2fa.ui.dashboard_ui
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

application_window: Gtk.ApplicationWindow = None
dashboard_ui: pi2fa.ui.dashboard_ui.DashboardUI = None


