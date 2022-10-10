import datetime
import logging
import pi2fa.ui.gtk.gtk_builder
import pi2fa.ui.gtk.gtk_css

import pi2fa.sms
import pi2fa.ui.DashboardSmsNotificationSignalHandler
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DashboardUI:
    '''Main Dashboard UI'''

    @property
    def gtk_application_window(self) -> Gtk.ApplicationWindow:
        '''Gtk required Application Window'''
        return self._gtk_application_window

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._builder = pi2fa.ui.gtk.gtk_builder.GtkBuilder(__file__, "dashboard.glade")
        self._gtk_application_window = self._builder.get_object("main_window")
        my_phone_number_national = pi2fa.data.config_data.PROFILE_DATA['my_phone_number_national']
        contact_label_text = "My Phone Number: {0}".format(my_phone_number_national)
        contact_label = self._builder.get_object("contact_label")
        contact_label.set_text(contact_label_text)
        css_file = "dashboard.css"
        css_parser = pi2fa.ui.gtk.gtk_css.GtkCss()
        css_parser.load_and_apply_css(__file__, css_file)

    def _create_sms_notification_ui_frame(self, gtk_builder: Gtk.Builder, sms_dto: pi2fa.sms.SmsDto) -> Gtk.Frame:
        '''Creates SMS Notification frame, which is inserted into Dashboard UI'''
        self._logger.debug("entered _create_sms_notification_ui_frame")

        #load ui temmplate
        glade_file_name = "sms_notification_frame.glade"
        gtk_builder.add_from_file(__file__, glade_file_name)
        frame = gtk_builder.get_object("sms_notification_frame")

        #data binding
        datetime_label = gtk_builder.get_object("datetime_label")
        datetime_label.set_text(sms_dto.timestamp.strftime("%a %b %d, %I:%M %p"))

        label_text = "New SMS from\n{0}".format(sms_dto.from_phone_number)

        sms_from_label = gtk_builder.get_object("new_sms_label")
        sms_from_label.set_text(label_text)

        sms_content_label = gtk_builder.get_object("sms_content_label")
        sms_content_label.set_text(sms_dto.content)

        # signal handler
        container = gtk_builder.get_object("notification_box")
        signal_hander = pi2fa.ui.DashboardSmsNotificationSignalHandler.DashboardSmsNotificationSignalHandler(
            container)
        gtk_builder.connect_signals(signal_hander)

        return frame

    def show_sms_notification(self, sms_dto: pi2fa.sms.SmsDto) -> None:
        '''Creates Frame, then inserts into Dashboard UI and shows'''
        frame = self._create_sms_notification_ui_frame(self._builder, sms_dto)
        notification_box = self._builder.get_object("notification_box")
        notification_box.pack_end(frame, False, False, 0)

    def show(self) -> None:
        '''Builds Window and child widgets'''
        self._gtk_application_window.show_all()

    def _close(self, unused) -> None:
        '''Shuts window'''
        self._gtk_application_window.close()