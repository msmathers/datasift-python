import httplib
from time import sleep
from socket import timeout

STREAM_HOST = "stream.datasift.com"
STREAM_URL = "/%s?username=%s&api_key=%s"
STREAM_TIMEOUT = 300
STREAM_HEADERS = {'Connection': 'Keep-Alive'}

class UncompiledDefinition(Exception): pass
class InvalidListener(Exception): pass


class DataSiftStream(object):
    '''Represents an HTTP stream from DataSift's Streaming API.
    Instantiate with a custom subclass of DataSiftStreamListener, as well as
    instances of DataStreamDefinition and DataSiftUser.'''
    def __init__(self, listener, definition, user, retry_delay=1.0):
        if definition.hash is None:
            raise UncompiledDefinition(str(definition))
        if not isinstance(listener, DataSiftStreamListener):
            raise InvalidListener(
              "Listener must be a subclass of DataSiftStreamListener")
        self.listener = listener
        self.definition = definition
        self.user = user
        self.running = False
        self._retry_delay = retry_delay
        self._errors = 0

    def listen(self):
        '''Public method to connect & listen to DataSift stream.'''
        conn = None
        exception = None
        self.running = True
        args = (self.definition.hash, self.user.username, self.user.api_key)
        stream_url = STREAM_URL % args
        while self.running:
            try:
                conn = httplib.HTTPConnection(STREAM_HOST)
                conn.connect()
                self.listener.on_connect()
                conn.sock.settimeout(STREAM_TIMEOUT)
                conn.request('GET', stream_url, headers=STREAM_HEADERS)
                resp = conn.getresponse()
                if resp.status != 200:
                    msg = resp.read()
                    if self.listener.on_error(msg, resp.status) is False:
                        break
                    self._errors += 1
                    self._sleep()
                else:
                    self._read(resp)
            except timeout:
                if self.listener.on_timeout() is False:
                    break
                if self.running is False:
                    break
                if conn:
                    conn.close()
                self._errors += 1
                self._sleep()
            except Exception as exception:
                self._disconnect(conn)
                raise

        self.running = False
        self._disconnect(conn)

    def _read(self, resp):
        while self.running:
            if resp.isclosed():
                break
            data = ''
            while True:
                c = resp.read(1)
                if c == '\n':
                    break
                data += c
            data = data.strip()
            if self.listener.on_data(data) is False:
                self.running = False

    def _sleep(self):
        sleep(self._retry_delay + self._errors)

    def _disconnect(self, conn):
        if conn:
            conn.close()
        self.listener.on_disconnect()


class DataSiftStreamListener(object):
    '''Defines a stream 'listener' with callback methods for specific events.
    Create a subclass and use it to instantiate a DataSiftStream.'''
    def on_connect(self):
        pass
    def on_data(self, data):
        pass
    def on_error(self, msg, status_code):
        pass
    def on_timeout(self):
        pass
    def on_disconnect(self):
        pass
