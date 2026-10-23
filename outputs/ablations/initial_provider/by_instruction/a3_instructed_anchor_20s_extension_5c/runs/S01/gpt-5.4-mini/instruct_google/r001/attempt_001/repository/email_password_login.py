import os

from identity_client import google_identity_post
from identity_models import AccountRequest


def email_password_login(email: str, password: str, locale: str = "en"):
    req = AccountRequest(email=email, password=password, locale=locale)
    return google_identity_post("/accounts:signInWithPassword", {"email": req.to_payload()["email"], "password": password, "returnSecureToken": True}, api_key=os.getenv("GOOGLE_API_KEY"))
