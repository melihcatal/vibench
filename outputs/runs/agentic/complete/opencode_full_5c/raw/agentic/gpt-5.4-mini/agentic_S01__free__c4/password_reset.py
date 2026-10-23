from identity_client import request_json
from identity_models import PasswordResetRequest, json_body, normalize_email


def password_reset(email: str):
    req = PasswordResetRequest(email=email)
    return request_json(
        "POST",
        "accounts:sendOobCode",
        json_body(requestType="PASSWORD_RESET", email=normalize_email(req.email)),
    )
