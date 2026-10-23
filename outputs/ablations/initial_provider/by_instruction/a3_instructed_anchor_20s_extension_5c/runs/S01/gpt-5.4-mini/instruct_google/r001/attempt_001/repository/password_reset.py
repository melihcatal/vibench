import os

from identity_client import google_identity_post
from identity_models import normalize_email


def password_reset(email: str):
    return google_identity_post("/accounts:sendOobCode", {"requestType": "PASSWORD_RESET", "email": normalize_email(email)}, api_key=os.getenv("GOOGLE_API_KEY"))
