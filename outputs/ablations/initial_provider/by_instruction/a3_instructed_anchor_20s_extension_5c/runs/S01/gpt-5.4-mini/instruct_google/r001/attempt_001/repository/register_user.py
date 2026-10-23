import os

from identity_client import google_identity_post
from identity_models import AccountRequest


def register_user(email: str, password: str, locale: str = "en"):
    req = AccountRequest(email=email, password=password, locale=locale)
    return google_identity_post("/accounts:signUp", req.to_payload(), api_key=os.getenv("GOOGLE_API_KEY"))
