from identity_client import post_json
from identity_models import IdentityResult, LoginRequest


def email_password_login(email: str, password: str) -> IdentityResult:
    request = LoginRequest(email=email, password=password)
    data = post_json("/responses", {"model": "gpt-5.4-mini", "input": request.normalized()})
    return IdentityResult(status="authenticated", data=data)
