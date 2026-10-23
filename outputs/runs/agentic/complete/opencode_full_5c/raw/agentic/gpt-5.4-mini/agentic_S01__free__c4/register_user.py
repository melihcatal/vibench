from identity_client import account_payload, request_json
from identity_models import RegisterUserRequest


def register_user(email: str, password: str, locale: str = "en", name: str = ""):
    req = RegisterUserRequest(email=email, password=password, locale=locale, name=name)
    return request_json(
        "POST",
        "accounts:signUp",
        account_payload(req.email, req.password, req.locale, req.name),
    )
