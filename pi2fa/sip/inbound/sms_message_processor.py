'''Processes Inbound Messages'''
import logging
import re
import datetime
import mimetypes

import requests

class InboundProcessor:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def process_sms_message(self, message_body):
        '''Processes SMS/MMS received from Twilio'''
        self._logger.debug("entered process_sms_message")
        message_lines = message_body.split('\n')
        message_first_line = message_lines[0]
        message_body = '\n'.join(message_lines[1:])
        from_phone_number = message_first_line.split('=')[1]
        self._logger.debug('from_phone_number = %s', from_phone_number)
        (message_stripped_of_links, links) = self._extract_links(message_body)
        message_body = message_stripped_of_links.strip()
        self._logger.debug("message_body after strip() = '%s'", message_body)
        self._logger.info("")

        if message_body != "":
            self._logger.debug("display_sms with message body %s", message_body)
        if len(links) > 0:
            for link in links:
                self._logger.debug("processing link %s", link)
                content_type = self._get_content_type(link)
                file_extension = mimetypes.guess_extension(content_type)
                self._logger.debug("link has content_type %s", content_type)
                self._logger.debug("link has extension %s", file_extension)
                if content_type in ['image/jpeg', 'image/gif', 'image/png']:
                    #auto display pictures for twilio fully supported media types
                    #https://www.twilio.com/docs/sms/accepted-mime-types
                    self._logger.debug("would auto display link")
                else:
                    self._logger.debug("not a supported picture, not auto displaying link.  Content type: '%s', link: '%s'", content_type, link)
        self.logger.info("SMS Message Received at %s.  Body is %s.  Links are %s", datetime.datetime.now(), message_body, links)

    def _extract_links(self, message_body):
        '''extracts twilio links from message_body'''
        self._logger.debug('entered extract_links')
        self._logger.debug("looking for links in message body '%s'", message_body)
        re_pattern = r"(https://api.twilio.com/.*?)\n"
        links = re.findall(re_pattern, message_body)
        self._logger.debug('found %d links', len(links))
        message_stripped_of_links = re.sub(re_pattern, '', message_body)
        self._logger.debug('removed links from message body')
        return (message_stripped_of_links, links)

    def _get_content_type(self, link):
        '''gets content type for a link.'''
        self._logger.debug("entered _get_content_type, link is '%s'", link)
        response = requests.head(link, allow_redirects=True)
        assert response is not None
        self._logger.debug("response.status_code=%s", response.status_code)
        assert response.status_code == 200
        content_type = response.headers['Content-Type']
        self._logger.debug("content_type = %s", content_type)
        return content_type
