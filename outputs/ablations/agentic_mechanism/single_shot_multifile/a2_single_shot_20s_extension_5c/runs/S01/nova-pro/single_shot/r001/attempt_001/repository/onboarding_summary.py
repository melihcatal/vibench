import os
from twilio.rest import Client

def send_summary(to, summary):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=summary,
        from_='+12345678901',
        to=to
    )
    return message.sid