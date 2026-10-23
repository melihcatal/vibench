from identity_client import post_json
from identity_models import IdentityResult, RefreshRequest


def refresh_session(refresh_token: str) -> IdentityResult:
    request = RefreshRequest(refresh_token=refresh_token)
    data = post_json("/responses", {"model": "gpt-5.4-mini", "input": request.normalized()})
    return IdentityResult(status="refreshed", data=data)
