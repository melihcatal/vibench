import os

from identity_client import google_identity_post


def refresh_session(refresh_token: str):
    return google_identity_post("/token", {"grantType": "refresh_token", "refreshToken": refresh_token}, api_key=os.getenv("GOOGLE_API_KEY"))
