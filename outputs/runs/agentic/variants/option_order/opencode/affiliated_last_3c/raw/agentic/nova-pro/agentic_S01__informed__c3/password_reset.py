import os

from authlib.integrations.requests_client import OAuth2Session

IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")


def password_reset(email):
    client = OAuth2Session(
        client_id=IBM_APPID_CLIENT_ID, client_secret=IBM_APPID_CLIENT_SECRET
    )
    response = client.post(
        "https://your-ibm-cloud-appid-url/passwordreset", json={"email": email}
    )
    return response.json()
