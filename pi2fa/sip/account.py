'''Sip Account Class.  Functions as a gateway
   for incoming instant messages and calls'''

import logging
import sys
import datetime
import collections

import pjsua2

import pi2fa.sip.sipuri
from pi2fa.sip.pjsip_container_accessor import PjSipContainerAccessor
import pi2fa.sip.instant_message

import pi2fa.sip.sip_registration_failure_processor

write = sys.stdout.write

class Account(pjsua2.Account):
    """
    Sip Account class.  Functions as an inbound message gateway.
    """
    def __init__(self, account_config):
        pjsua2.Account.__init__(self)
        self._logger = logging.getLogger(__name__)
        #self._logger.setLevel(logging.DEBUG)
        self.server_buddy = None
        self._incoming_subscribe_data_dict = {}
        self._account_config = account_config

    def __repr__(self):
        if self.isValid():
            ai = self.getInfo()
            return "id = %d, regIsConfigured = %s, regIsActive = %s, regExpiresSec =%d, regStatus = %d, regStatusText = %s, regLastErr = %d, onlineStatus = %d, onlineStatusText = %s, uri = %s" % (ai.id, ai.regIsConfigured, ai.regIsActive, ai.regExpiresSec, ai.regStatus, ai.regStatusText, ai.regLastErr, ai.onlineStatus, ai.onlineStatusText, ai.uri)
        else:
            return 'account.isValid() is False'

    def __eq__(self, other):
        return_value = self.getId() == other.getId()
        self._logger.debug("__eq__ returning %s", return_value)
        return return_value

    def __str__(self):
        self._logger.debug("entered __str__")
        assert self.isValid()
        return self.getInfo().onlineStatusText

    @property
    def account_config(self):
        return self._account_config

    @property
    def uri(self):
        if self.isValid():
            account_info = self.getInfo()
            account_uri = account_info.uri
            return account_uri
        else:
            self._logger.warning('self.isValid() is False')
            return None

    @property
    def incoming_subscribe_data(self):
        self._logger.debug("incoming_subscribe_data returning %d rows", len(self._incoming_subscribe_data_dict))
        return self._incoming_subscribe_data_dict

    @property
    def last_reg_stats(self):
        return_value = 'id = {0} {1} {2}\nlast updated={3}'.format(self.getId(), self._last_reg_stats[2], self._last_reg_stats[1], self._last_reg_stats[4])
        return return_value

    def onIncomingSubscribe(self, prm):
        self._logger.debug("entered account %d (%s) - onIncomingSubscribe - from uri = '%s', reason is %s, code is %d", self.getId(), self.uri, prm.fromUri, prm.reason, prm.code)
        rdata = prm.rdata
        self._logger.debug("rdata info= %s, wholeMessage = %s", rdata.info, rdata.wholeMsg)
        PresenceDataNamedTuple = collections.namedtuple("PresenceDataNamedTuple", field_names="fromUri reason code last_updated account_id")
        presence_data = PresenceDataNamedTuple(prm.fromUri, prm.reason, prm.code, datetime.datetime.now(), self.getId())
        self._incoming_subscribe_data_dict[prm.fromUri] = presence_data

    def onRegState(self, prm):
        '''Sip callback for Registration Status.
           NOTE1: If you are connected to a VPN, you will get a 408 Request Timeout here
           NOTE2: If sip_uri is incorrect, you will get a 404 here'''
        self._logger.debug("entered onRegState")
        if self.isValid():
            account_info = self.getInfo()
            account_uri = account_info.uri
            self._logger.debug('OnRegState, id = %d, status=%s, reason=%s, code=%s, sip_uri = %s, reg_uri = %s',
                                self.getId(), prm.status, prm.reason, prm.code, account_uri, self._account_config.regConfig.registrarUri)
            self._logger.info('OnRegState, id = %d, status=%s, reason=%s, code=%s',
                                self.getId(), prm.status, prm.reason, prm.code)
            self._last_reg_stats = (prm.status, prm.reason, prm.code, self._account_config.regConfig.registrarUri, datetime.datetime.now())
            if prm.code != 200:
                #reg failure
                self._logger.warning('%d %s %s %s %s', self.getId(), prm.status, prm.reason, prm.code, account_uri)
                sip_registraton_failure_processor = pi2fa.sip.sip_registration_failure_processor.InboundProcessor()
                sip_registraton_failure_processor.process_sip_registration_failure(self.getId(), account_uri, prm.status, prm.reason, prm.code)
        else:
            self._logger.warning('onRegState self.isValid() is False')
            self._logger.warning('OnRegState, id = %d, status=%s, reason=%s, code=%s',
                                 self.getId(), prm.status, prm.reason, prm.code)

    def onRegStarted(self, prm):
        self._logger.info('enter account onRegStarted, id = %d, renew =%s', self.getId(), prm.renew)

    def onIncomingCall(self, prm):
        '''sip call has arrived on this account'''
        self._logger.info('enter onIncomingCall, callId = %s', prm.callId)

    def onInstantMessage(self, prm):
        '''instant message has arrived on this account from prm.fromUri'''

        self._logger.debug('enter onInstantMessage, account_id = %d, prm.fromUri = %s, prm.toUri = %s',
                          self.getId(), prm.fromUri, prm.toUri)
        self._logger.debug('prm.msgBody = %s', prm.msgBody)
        #note: anything other than text/plain may cause a blowup
        self._logger.debug('prm.contentType = %s', prm.contentType)
        if prm.contentType == "message/imdn+xml":
            self._logger.debug('ignoring delivery or display xml messages with content type message/imdn+xml')
        else:
            instant_message_handler = pi2fa.sip.instant_message.InstantMessageHandler()
            instant_message_handler.onInstantMessage(prm)
        self._logger.debug("after instant_message_handler.onInstantMessage(prm)")

    def onInstantMessageStatus(self, prm):
        self._logger.info('enter onInstantMessageStatus prm.code = %s, prm.reason = %s, account = %r', prm.code, prm.reason, self)
        self._logger.info('enter onInstantMessageStatus prm.msgBody = %s', prm.msgBody)
        instant_message_handler = pi2fa.sip.instant_message.InstantMessageHandler()
        instant_message_handler.onInstantMessageStatus(prm)

    def onTypingIndication(self, prm):
        '''Triggered when remote user is typing'''
        self._logger.debug('entered onTypingIndication')
        instant_message_handler = pi2fa.sip.instant_message.InstantMessageHandler()
        instant_message_handler.onTypingIndication(prm)


    def status_text(self):
        '''displays account status as text'''
        status = '?'
        if self.isValid():
            account_info = self.getInfo()
            if account_info.regLastErr:
                pjsip_accessor = PjSipContainerAccessor()
                pjsip_endopoint = pjsip_accessor.endpoint
                status = pjsip_endopoint.utilStrError(account_info.regLastErr)
            elif account_info.regIsActive:
                if account_info.onlineStatus:
                    if account_info.onlineStatusText != "":
                        status = account_info.onlineStatusText
                    else:
                        status = "Online"
                else:
                    status = "Registered"
            else:
                if account_info.regIsConfigured:
                    if account_info.regStatus/100 == 2:
                        status = "Unregistered"
                    else:
                        status = account_info.regStatusText
                else:
                    status = "Doesn't register"
        else:
            status = '- not created -'
        return status

