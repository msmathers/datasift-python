DataSift Python Client Library
==============================

This is an *unofficial* Python library for [Datasift](http://datasift.com/).

It currently supports compiling CSDLs via the REST API and consuming an HTTP Stream via the Streaming API.

Requirements
------------

* [requests](https://github.com/kennethreitz/requests)

Example
-------

```python
from datasift import (
  DataSiftUser,
  DataSiftDefinition,
  DataSiftStream,
  DataSiftStreamListener
)

# Fill in account credentials
DATASIFT_USERNAME = "my_username"
DATASIFT_API_KEY = "my_api_key"

# Create user
user = DataSiftUser(DATASIFT_USERNAME, DATASIFT_API_KEY)

# Create, compile CSDL
csdl = 'interaction.type == "twitter" and '\
  '(interaction.content contains "skrillex")'
definition = DataSiftDefinition(csdl, user)
definition.compile()

# Define listener
class MyListener(DataSiftStreamListener):
    def on_data(self, data):
        print data

# Create stream, listen
listener = MyListener()
stream = DataSiftStream(listener, definition, user)
stream.listen()
```

License
-------

All code is released under the MIT license.  Please read the LICENSE.txt file for more details.

Acknowledgements
----------------

Thanks to [joshthecoder](https://github.com/joshthecoder) and his [tweepy](https://github.com/tweepy/tweepy) library for demonstrating HTTP stream consumption via httplib.