import json
import requests

API_HOST = "api.datasift.com"

class ValidationError(Exception): pass


class DataSiftDefinition(object):
    '''Represents a stream definition.  Validates & compiles
    CSDL strings for the stream consumer.'''
    def __init__(self, csdl, user):
        self.csdl = csdl
        self.user = user
        self.dpu = None
        self.created_at = None
        self.hash = None

    def __str__(self):
        return "%s (%s)" % (self.csdl, self.hash or "<Uncompiled>")

    def __request(self, url):
        params = {
          'csdl': self.csdl,
          'username': self.user.username,
          'api_key': self.user.api_key
        }
        url = "http://%s/%s" % (API_HOST, url)
        res = requests.get(url, params=params)
        rdata = json.loads(res.content)
        if res.status_code != 200 or 'error' in rdata:
            msg = rdata.get('error', res.content)
            raise ValidationError(msg)
        return rdata

    def set(self, csdl):
        self.csdl = csdl
        self.dpu = None
        self.created_at = None
        self.hash = None

    def validate(self):
        rdata = self.__request('validate')
        self.dpu = rdata['dpu']
        self.created_at = rdata['created_at']
        return rdata

    def compile(self):
        rdata = self.__request('compile')
        self.dpu = rdata['dpu']
        self.created_at = rdata['created_at']
        self.hash = rdata['hash']
        return rdata

