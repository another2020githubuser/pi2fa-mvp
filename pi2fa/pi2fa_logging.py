import logging

#set up logging
date_fmt = '%Y-%m-%d,%H:%M:%S'
log_format = '%(levelname)s %(asctime)s.%(msecs)03d %(threadName)s %(name)s.%(funcName)s %(message)s'
logging.basicConfig(format=log_format, datefmt=date_fmt, level=logging.DEBUG)
_logger = logging.getLogger(__name__)
_logger.debug('logging initialized')