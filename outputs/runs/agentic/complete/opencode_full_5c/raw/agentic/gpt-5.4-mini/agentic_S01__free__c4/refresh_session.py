from identity_client import request_json
from identity_models import RefreshRequest, json_body


def refresh_session(refresh_token: str):
    req = RefreshRequest(refresh_token=refresh_token)
    return request_json(
        "POST",
        "token",
        json_body(grant_type="refresh_token", refresh_token=req.refresh_token),
    )
