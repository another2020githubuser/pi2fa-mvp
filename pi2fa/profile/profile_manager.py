'''Retrieves profile'''
import logging
import json
import os

import requests
import phonenumbers

import pi2fa.data.config_data
import pi2fa.ui.gtk.gtk_dialog

class ProfileManager:
    '''gets profile'''
    def __init__(self):
        self._logger = logging .getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

    def get_profile(self, phone_number:str=None) -> dict:
        '''downloads profile'''
        self._logger.debug("entered get_profile")

        profile_url = os.environ['PROFILE_URL']
        self._logger.debug('profile_url = %s', profile_url)
        username = os.environ['USERNAME']
        self._logger.debug('username = %s', username)
        password = os.environ['PASSWORD']
        self._logger.debug('password = %s', password)
        if phone_number is None:
            phone_number = os.environ['PHONE_NUMBER']
        self._logger.debug('phone_number = %s', phone_number)
        data = {
            'username': username,
            'password': password,
            'phone_number' : phone_number
        }

        response = None
        user_profile = None
        try:
            response = requests.post(profile_url, data=data, timeout=10)
            self._logger.debug("response.status_code = %s", response.status_code)
        except requests.exceptions.ConnectionError as connection_error:
            self._logger.error(connection_error)
            response = None
        self._logger.debug("after requests.post")

        if response is None:
            self._logger.info("response is None")
            dialog_main_text = "Fatal: Profile Download Failed"
            dialog_secondary_text = "Fatal Error, Profile Download Failed"
            simple_dialog = pi2fa.ui.gtk.gtk_dialog.CommonDialogs()
            simple_dialog.show_info_dialog(dialog_main_text, dialog_secondary_text, None)
        else:
            self._logger.info("response.status_code == %s", response.status_code)
            if response.status_code == 200:
                download_content = response.content
                self._logger.debug('download_content = %s', download_content)
                user_profile = json.loads(download_content.decode('utf-8'))
                self._logger.debug("user_profile = %s", user_profile)
                parsed_number = phonenumbers.parse(user_profile['my_phone_number'], user_profile['phone_number_region'])
                my_phone_number_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
                self._logger.debug("my_phone_number_national = %s", my_phone_number_national)
                user_profile['my_phone_number_national'] = my_phone_number_national
                pi2fa.data.config_data.PROFILE_DATA = user_profile
                self._logger.info("profile download success")
                return user_profile
            else:
                self._logger.info("Unexpected response.status_code == %s", response.status_code)
                download_content = response.content
                self._logger.debug('download_content = %s', download_content)
                dialog_main_text = "Fatal: Profile Download Error # {0}".format(response.status_code)
                dialog_secondary_text = "Fatal Error, Profile Download Error # {0}".format(response.status_code)
                simple_dialog = pi2fa.ui.gtk.gtk_dialog.CommonDialogs()
                simple_dialog.show_info_dialog(dialog_main_text, dialog_secondary_text, None)
