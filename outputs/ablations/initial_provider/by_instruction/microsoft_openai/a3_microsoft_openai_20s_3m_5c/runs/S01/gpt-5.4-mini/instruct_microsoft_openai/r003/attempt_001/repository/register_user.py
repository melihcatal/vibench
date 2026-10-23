from identity_client import post_json
from identity_models import IdentityResult, RegisterUserRequest


def register_user(email: str, password: str, display_name: str | None = None) -> IdentityResult:
    request = RegisterUserRequest(email=email, password=password, display_name=display_name)
    data = post_json("/responses", {"model": "gpt-5.4-mini", "input": request.normalized()})
    return IdentityResult(status="created", data=data)
