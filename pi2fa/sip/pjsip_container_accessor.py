'''Used to access sip_container'''

import logging
import pi2fa.sip.sip_container
import pjsua2

class PjSipContainerAccessor:
    '''wrapper to provide a standard way to access module scope pj sip variables'''
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @property
    def endpoint(self) -> pjsua2.Endpoint:
        '''retrns pjsip endpoint.  Throws exception if not initialized.  
           Failure to initialize is sip config/network issue'''
        #don't log entrance here because pjsip polls every 50 msec...
        assert pi2fa.sip.sip_container.sip_container is not None
        assert pi2fa.sip.sip_container.sip_container.ep is not None
        pjsip_endpoint = pi2fa.sip.sip_container.sip_container.ep
        assert pjsip_endpoint is not None
        return pjsip_endpoint

    @property
    def sip_account_list(self): #-> list[pjsua2.Account]:  pyLance objected to list
        return pi2fa.sip.sip_container.sip_container.sip_account_list

    @property
    def pjsip_log_writer(self) -> pjsua2.LogWriter:
        return pi2fa.sip.sip_container.sip_container.pjsip_log_writer