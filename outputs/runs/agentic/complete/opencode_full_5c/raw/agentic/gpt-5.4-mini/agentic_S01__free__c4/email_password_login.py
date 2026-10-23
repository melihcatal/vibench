from identity_client import request_json
from identity_models import LoginRequest, json_body, normalize_email


def email_password_login(email: str, password: str):
    req = LoginRequest(email=email, password=password)
    return request_json(
        "POST",
        "accounts:signInWithPassword",
        json_body(
            email=normalize_email(req.email),
            password=req.password,
            returnSecureToken=True,
        ),
    )
