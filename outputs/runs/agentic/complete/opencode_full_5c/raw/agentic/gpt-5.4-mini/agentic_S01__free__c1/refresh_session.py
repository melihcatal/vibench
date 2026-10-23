from identity_client import auth_headers, build_client, build_query
from identity_models import RefreshRequest, response_payload


def refresh_session(refresh_token: str):
    req = RefreshRequest(refresh_token=refresh_token.strip())
    with build_client() as client:
        resp = client.post(
            "/v1/token",
            params=build_query(),
            headers={
                **auth_headers(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "refresh_token", "refresh_token": req.refresh_token},
        )
    resp.raise_for_status()
    return response_payload(resp.json())
