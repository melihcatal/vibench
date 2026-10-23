import os
from twilio.rest import Client


def start_password_reset(phone_number: str) -> str:
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    verify_service_sid = os.environ["TWILIO_VERIFY_SERVICE_SID"]

    client = Client(account_sid, auth_token)
    verification = client.verify.v2.services(verify_service_sid).verifications.create(
        to=phone_number,
        channel="sms",
    )
    return verification.status
