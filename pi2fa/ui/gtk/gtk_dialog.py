'''simple gtk canned dialogs'''
import logging
import os.path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk # pylint: disable=wrong-import-position

class CommonDialogs:
    '''Gtk wrapper for some simple dialog types'''

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def show_info_dialog(self, main_text, secondary_text, parent=None, title=None):
        '''Displays a Gtk Info Dialog'''
        self._logger.debug("entered show_info_dialog")
        dialog_main_text = main_text
        dialog_secondary_text = secondary_text
        flags = 0
        parent_window = parent
        dialog = Gtk.MessageDialog(parent_window, flags, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, dialog_main_text)
        if title is not None:
            self._logger.debug("setting title to %s", title)
            dialog.set_title(title)
        dialog.format_secondary_text(dialog_secondary_text)
        dialog.run()
        dialog.destroy()

    def show_ok_cancel_dialog(self, title, main_text, secondary_text, parent=None):
        '''Displays a Gtk OK/Cancel Dialog'''
        self._logger.debug("entered show_ok_cancel_dialog")
        dialog_main_text = main_text
        dialog_secondary_text = secondary_text
        flags = 0
        parent_window = parent
        dialog = Gtk.MessageDialog(parent_window, flags, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, dialog_main_text, title=title)
        dialog.format_secondary_text(dialog_secondary_text)
        response = dialog.run()
        dialog.destroy()
        self._logger.debug("show_ok_cancel_dialog returning %s", response)
        assert response in [Gtk.ResponseType.OK, Gtk.ResponseType.CANCEL]
        return response


    def show_file_open_dialog(self, parent_window):
        '''Shows File Open Dialog.  Returns file name'''
        self._logger.debug('entered show_file_open_dialog')

        file_open_dialog = Gtk.FileChooserDialog("Open...",
                                                 parent_window,
                                                 Gtk.FileChooserAction.OPEN,
                                                 (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                  Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog_response = file_open_dialog.run()
        self._logger.debug("dialog_response = %s", dialog_response)
        local_file = file_open_dialog.get_filename()
        self._logger.debug("local file: %s", local_file)
        file_open_dialog.destroy()
        return (dialog_response, local_file)
