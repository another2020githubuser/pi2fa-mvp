'''pj sip logging module'''
#TODO: rename this to pjsip_logger.py

import logging #python logger, not pjsip logger

import pjsua2 as pj

class PjLogger(pj.LogWriter):
    """
    Logger to receive log messages from pjsua2
    """
    def __init__(self):
        pj.LogWriter.__init__(self)
        self._logger = logging.getLogger(__name__)
        self._logger.debug('PjLogger constructor')
        self._logger.setLevel(logging.INFO)

    def write(self, entry):
        self._logger.debug("%d %d %s %s", entry.level, entry.threadId, entry.threadName, entry.msg)
        #print(entry.level, entry.threadId, entry.threadName, str(entry.msg))
        