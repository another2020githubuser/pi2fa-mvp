import datetime

class SmsDto:
    '''Model class for SMS'''
    def __init__(self, timestamp: datetime.datetime, from_phone_number: str, content: str):
        self._from_phone_number = from_phone_number
        self._timestamp = timestamp
        self._content = content

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def from_phone_number(self):
        return self._from_phone_number

    @property
    def content(self):
        return self._content
