'''Processes Sip Registration Failures'''
import logging

class InboundProcessor:
    '''Processes Sip Registration Failure'''

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def process_sip_registration_failure(self, account_id, account_uri, status, reason, code):
        '''Shows notification when sip registration fails'''
        self._logger.debug("Entered process_sip_registration_failure")

        self._logger.warning("SIP registration failure: account_id=%s, account_uri=%s, status=%s, reason=%s, code=%s", account_id, account_uri, status, reason, code)
