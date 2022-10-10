'''Manages stateful sip objects'''

import logging

import pjsua2

import pi2fa.sip.logger
import pi2fa.sip.sip_container
import pi2fa.sip.account
import pi2fa.data.config_data

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib

#TODO:  enforce this class as a singleton
class SipLifeCycleManager:
    '''manages sip objects lifecycle'''
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        #self._logger.setLevel(logging.DEBUG)
        #TODO: SipLifeCycleManager must be a singleton
        self._total_event_count = 0

    @property
    def total_event_count(self) -> int:
        return self._total_event_count

    def startup(self) -> None:
        '''starts up sip'''
        self._logger.debug("entered startup()")
        #create pjsip endpoint
        ep_cfg = pjsua2.EpConfig()
        ep_cfg.uaConfig.mainThreadOnly = True
        ep_cfg.uaConfig.threadCnt = 0
        ep_cfg.uaConfig.userAgent = "not yet set - fixme"
        self._logger.debug('ep_cfg.uaConfig.userAgent = %s', ep_cfg.uaConfig.userAgent)
        ep_cfg.logConfig.msgLogging = 1

        # /**
        #  * Declare maximum logging level/verbosity. Lower number indicates higher
        #  * importance, with the highest importance has level zero. The least
        #  * important level is five in this implementation, but this can be extended
        #  * by supplying the appropriate implementation.
        #  *
        #  * The level conventions:
        #  *  - 0: fatal error
        #  *  - 1: error
        #  *  - 2: warning
        #  *  - 3: info
        #  *  - 4: debug
        #  *  - 5: trace
        #  *  - 6: more detailed trace
        #  *
        #  * Default: 4
        #  */

        ep_cfg.logConfig.level = 6
        ep_cfg.logConfig.consoleLevel = 6
        decor = pjsua2.PJ_LOG_HAS_YEAR | \
                pjsua2.PJ_LOG_HAS_MONTH | \
                pjsua2.PJ_LOG_HAS_DAY_OF_MON | \
                pjsua2.PJ_LOG_HAS_TIME | \
                pjsua2.PJ_LOG_HAS_MICRO_SEC | \
                pjsua2.PJ_LOG_HAS_SENDER | \
                pjsua2.PJ_LOG_HAS_NEWLINE | \
                pjsua2.PJ_LOG_HAS_SPACE | \
                pjsua2.PJ_LOG_HAS_THREAD_SWC | \
                pjsua2.PJ_LOG_HAS_INDENT
        self._logger.debug('decor = %s', decor)
        ep_cfg.logConfig.decor = decor
        ep_cfg.logConfig.filename = "logs/sip.log"
        ep_cfg.logConfig.fileFlags = pjsua2.PJ_O_APPEND
        #don't combine the next 2 statements
        pjsip_log_writer = pi2fa.sip.logger.PjLogger()
        ep_cfg.logConfig.writer = pjsip_log_writer
        sip_container = pi2fa.sip.sip_container.sip_container
        sip_container.pjsip_log_writer = pjsip_log_writer
        sip_container.ep = pjsua2.Endpoint()
        ep = sip_container.ep
        ep.libCreate()
        ep.libInit(ep_cfg) #if this fails, usually logs folder does not exist
        pjsip_version = ep.libVersion().full
        self._logger.debug('pjsip_version = %s', pjsip_version)

        #create udp transport
        sip_udp_tranport_config = pjsua2.TransportConfig()
        sip_udp_tranport_config.port = 5060
        sip_udp_tranport_config.enabled = 1
        ep.transportCreate(pjsua2.PJSIP_TRANSPORT_UDP, sip_udp_tranport_config)
        self._logger.debug("transport created")

        #create sip account
        acfg = pjsua2.AccountConfig()
        acfg.idUri = pi2fa.data.config_data.PROFILE_DATA['sip_uri']
        acfg.regConfig.registrarUri = pi2fa.data.config_data.PROFILE_DATA['sip_registrar_uri']
        acfg.regConfig.registerOnAdd = True
        acfg.regConfig.timeoutSec = 60 #60 seconds
        acfg.regConfig.retryIntervalSec = 60
        aci = pjsua2.AuthCredInfo()
        aci.scheme = "digest"
        aci.realm = "*"
        aci.username = pi2fa.data.config_data.PROFILE_DATA['sip_username']
        aci.dataType = 0
        aci.data = pi2fa.data.config_data.PROFILE_DATA['sip_password']
        aciv = pjsua2.AuthCredInfoVector()
        aciv.append(aci)
        acfg.sipConfig.authCreds = aciv
        sip_container.sip_account_list.append(pi2fa.sip.account.Account(acfg))
        sip_account = sip_container.sip_account_list[0]
        sip_account.cfg = acfg
        sip_account.create(acfg, True)
        presence_status = pjsua2.PresenceStatus()
        presence_status.status = pjsua2.PJSUA_BUDDY_STATUS_ONLINE
        sip_account.setOnlineStatus(presence_status)
        self._logger.debug("sip account created: %r", sip_account)

        ep.libStart()
        self._logger.debug("after libStart()")
        self._source_tag = GLib.timeout_add(50, self.poll_sip_events_timer, False)
        self._logger.debug("started polling, source tag is %s", self._source_tag)


    def poll_sip_events_timer(self, quitting: bool) -> bool:
        '''polls for pending events every 50 msec'''

        if quitting:
            self._logger.debug("quitting detected, terminating polling, source tag is %s", self._source_tag)
            #if this assert fires, then there are multiple instances of this class.  It needs to be a singleton.
            assert self._source_tag is not None
            GLib.source_remove(self._source_tag)
            self._logger.debug("removed source tag")
            self._source_tag = None
            #although returning False from a timer is supposed to stop subsequent calls
            #it does not.  Only removing the source tag does that.
            return False
        else:
            #poll for events every 50 msec

            #NOTE: this routine makes duplicate assignments, and is pretty inefficient
            #TODO: fix this

            pjsip_endpoint = pi2fa.sip.sip_container.sip_container.ep

            #keep timeout in libHandleEvents set at 10msec or ui will get sluggish
            event_count = pjsip_endpoint.libHandleEvents(10)
            self._total_event_count += event_count
            if event_count < 0:
                self._logger.error("libHandleEvents returned %s", event_count)
            elif event_count > 3:
                self._logger.debug('event_count current = %d, total = %d', event_count, self._total_event_count)
            if event_count > 0 and self._total_event_count % 10 == 0:
                self._logger.debug("%d total events processed", self._total_event_count)
            return True

    def shutdown(self) -> None:
        '''shuts down sip and deallocates variables'''
        self._logger.debug('entered shutdown')
        #begin shut down

        #get rid of accounts
        sip_container = pi2fa.sip.sip_container.sip_container
        while sip_container.sip_account_list:
            account = sip_container.sip_account_list.pop()
            if account.server_buddy is not None:
                self._logger.debug("deleting buddy %r", account.server_buddy)
                account.server_buddy = None
            self._logger.debug("deleting acc %r", account)
            account = None
        self._logger.debug("accounts deleted")

        sip_container.sip_account_list = None
        self._logger.debug('removed accounts')

        sip_container.ep.libDestroy()
        self._logger.debug('pjsip endpoint destroyed')

        #stop event polling.  This must be done after sip is shut down or
        #pending events won't be processed
        self.poll_sip_events_timer(True)
        self._logger.debug("timer stopped")

        self._logger.debug("total events processed = %d", self._total_event_count)
        sip_container.ep = None
        sip_container.pjsip_log_writer = None
        sip_container = None
        self._logger.debug('exiting shutdown')

