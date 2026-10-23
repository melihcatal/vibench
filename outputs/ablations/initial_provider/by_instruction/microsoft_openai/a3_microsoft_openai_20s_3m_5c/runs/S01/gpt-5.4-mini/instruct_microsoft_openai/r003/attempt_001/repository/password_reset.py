from identity_client import post_json
from identity_models import IdentityResult, PasswordResetRequest


def password_reset(email: str) -> IdentityResult:
    request = PasswordResetRequest(email=email)
    data = post_json("/responses", {"model": "gpt-5.4-mini", "input": request.normalized()})
    return IdentityResult(status="reset_started", data=data)
