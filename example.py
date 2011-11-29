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