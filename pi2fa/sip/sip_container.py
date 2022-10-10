''' Sip has some static variables (endpoint, accounts, account config)
    that must be instantiated, kept alive and destroyed in a strict
    manner.  This module manages that process'''

import logging

import pjsua2

class SipContainer:
    '''
    Container for sip global variables.
    This is instantiated in init_pjsip_globals
    and should be accessed via pjsip_static_accessor
    '''

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.debug("PjSipContainer constructor")
        self.ep = None
        self.sip_account_list = []
        self.pjsip_log_writer = None

sip_container = None
if  sip_container is None:
    sip_container = SipContainer()
else:
    raise ValueError("Cannot reinitiailze sip_container")

