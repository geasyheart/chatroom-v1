from datetime import datetime


class DateTime(object):
    @classmethod
    def today(cls):
        now = datetime.now()
        return now.year * 10000 + now.month * 100 + now.day

    @classmethod
    def timestamp(cls):
        now = datetime.now()
        return int(now.timestamp())
