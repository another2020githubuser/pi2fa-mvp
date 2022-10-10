'''Signal Handler for SMS Notifications'''
import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DashboardSmsNotificationSignalHandler:
    '''Signal Handler for SMS Notifications'''
    def __init__(self, container):
        self._logger = logging.getLogger(__name__)
        self._container = container

    def on_close_button_click(self, frame: Gtk.Frame, user_data):
        '''UI callback, invoked when user clicks "X" in frame.  Closes frame.'''
        self._logger.debug("entered on_close_button_click")
        self._container.remove(frame)

