from __future__ import annotations

from identity_client import firebase_post
from identity_models import LoginRequest, normalize_token_response


def email_password_login(request: LoginRequest):
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }
    response = firebase_post("accounts:signInWithPassword", payload)
    return normalize_token_response(response)
