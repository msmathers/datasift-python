class DataSiftUser(object):
    '''Represents a DataSift user account.'''
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
    
    def __str__(self):
        return "%s (%s)" % (self.username, self.api_key)