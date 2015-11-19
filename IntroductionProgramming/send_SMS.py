# part of the Udacity course "Introduction to Programming"

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
with open('AccountSID.sec', 'r') as f:
    account_sid = f.read().strip()
with open('auth_token.sec', 'r') as f:
    auth_token = f.read().strip()
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+85261950675", from_="+12513336558",
                                 body="My first Twilio SMS!")
