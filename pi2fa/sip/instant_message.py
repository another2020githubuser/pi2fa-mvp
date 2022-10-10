'''Handles inbound SMS'''

import logging
import datetime
from pi2fa.sms import SmsDto
import pi2fa.ui.gtk.state
from pi2fa.sip.sipuri import UriValidator

class InstantMessageHandler:
    '''Instant Message Handler'''

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def onInstantMessage(self, prm):  # pylint: disable=invalid-name
        '''triggered when an instant message is received'''
        self._logger.debug('prm.msgBody = %s', prm.msgBody)
        # note: anything other than text/plain may cause a blowup
        self._logger.debug('prm.contentType = %s', prm.contentType)
        sip_uri_validator = UriValidator()

        is_valid_sip_uri = sip_uri_validator.validateSipUri(prm.fromUri)
        if not is_valid_sip_uri:
            self._logger.debug(
                '%s is not a valid sip uri, exiting', prm.fromUri)
            return

        message_body = prm.msgBody
        message_lines = message_body.split('\n')
        message_first_line = message_lines[0]
        if message_first_line.startswith("x-pyphone-received-from-number="):
            self._logger.info("New SMS Message")
            message_body = '\n'.join(message_lines[1:])
            from_phone_number = message_first_line.split('=')[1]
            self._logger.debug('from_phone_number = %s', from_phone_number)
            sms_dto = SmsDto(datetime.datetime.now(), from_phone_number, message_body)
            dashboard_ui = pi2fa.ui.gtk.state.dashboard_ui
            dashboard_ui.show_sms_notification(sms_dto)
        else:
            self._logger.info("SIP Message received: '%s'", prm.msgBody)

    def onInstantMessageStatus(self, prm):  # pylint: disable=invalid-name
        '''triggered by when instant message status changes'''
        self._logger.debug(
            'enter onInstantMessageStatus prm.code = %s, prm.reason = %s', prm.code, prm.reason)


