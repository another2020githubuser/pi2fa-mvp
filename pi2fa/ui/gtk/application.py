import logging
import pi2fa.sip.sip_lifecycle_manager
import pi2fa.ui.dashboard_ui
import pi2fa.ui.gtk.state
import pi2fa.profile.profile_manager
import pi2fa.data.config_data

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class Application(Gtk.Application):
    '''Gtk Application Initialization.'''

    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self._logger = logging.getLogger(__name__)
        self._logger.debug("Gtk Version Information: major:%s, minor:%s, micro: %s",
                           Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)

    def do_startup(self):
        '''Gtk.Application signal handler'''
        self._logger.debug('entered do_startup')
        Gtk.Application.do_startup(self)
        self._mgr = pi2fa.sip.sip_lifecycle_manager.SipLifeCycleManager()
        self._create_app_action("show_about_dialog", self._show_about_dialog)

    def do_activate(self, *args):
        '''Gtk.Application signal handler'''
        self._logger.debug('entered do_activate')
        Gtk.Application.do_activate(self)
        profile_manager = pi2fa.profile.profile_manager.ProfileManager()
        user_profile = profile_manager.get_profile()
        if user_profile is None:
            self._logger.warning("Profile Download Failed")
        else:
            self._logger.info("Profile download success")
            pi2fa.data.config_data.PROFILE_DATA = user_profile           
            # start up pjsip and store pjsip variables in a static structure
            dashboard_ui = pi2fa.ui.dashboard_ui.DashboardUI()
            pi2fa.ui.gtk.state.dashboard_ui = dashboard_ui
            #TODO: do I need to store application window or is dashboard_ui enough?
            pi2fa.ui.gtk.state.application_window = dashboard_ui.gtk_application_window
            pi2fa.ui.gtk.state.application_window.set_application(application=self)
            pi2fa.ui.gtk.state.dashboard_ui.show()
            self._mgr.startup()
            self._logger.info('Communication Layer Startup Success')        

    def do_shutdown(self):
        '''Gtk.Application signal handler'''
        self._logger.debug('entered do_shutdown')
        Gtk.Application.do_shutdown(self)
        self._mgr.shutdown()

    def _create_app_action(self, action_name, action_target_function) -> None:
        '''Creates a single Gtk SimpleAction'''
        self._logger.debug("entered _create_app_action. action_name = %s", action_name)
        simple_action = Gio.SimpleAction.new(action_name)
        simple_action.connect("activate", action_target_function)
        self.add_action(simple_action)

    def _show_about_dialog(self, action, user_data) -> None:
        '''Shows about dialog.'''
        self._logger.debug("entered _show_about_dialog. action = %s, user_data = %s", action, user_data)
        version = "22.10"
        dialog_main_text = "Pi2FA MVP Version: {0}".format(version)
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, dialog_main_text)
        dialog.set_title("About Pi2FA")
        dialog.run()
        dialog.destroy()