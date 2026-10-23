import os

from authlib.integrations.requests_client import OAuth2Session

IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")


def register_user(email, password):
    client = OAuth2Session(
        client_id=IBM_APPID_CLIENT_ID, client_secret=IBM_APPID_CLIENT_SECRET
    )
    token = client.fetch_token(
        token_url="https://your-ibm-cloud-appid-url/token",
        username=email,
        password=password,
    )
    return token
