import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def get_client():
    return {
        "client_id": "YOUR_GOOGLE_CLIENT_ID",
        "client_secret": "YOUR_GOOGLE_CLIENT_SECRET",
        "redirect_uri": "YOUR_REDIRECT_URI",
    }


def get_scopes():
    return ["openid", "email", "profile"]
