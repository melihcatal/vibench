import os

IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")


def get_client():
    from authlib.integrations.requests_client import OAuth2Session

    return OAuth2Session(
        client_id=IBM_APPID_CLIENT_ID, client_secret=IBM_APPID_CLIENT_SECRET
    )
