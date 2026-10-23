from __future__ import annotations

from identity_client import firebase_post
from identity_models import RegistrationRequest, normalize_registration_response


def register_user(request: RegistrationRequest):
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }
    response = firebase_post("accounts:signUp", payload)
    return normalize_registration_response(response)
