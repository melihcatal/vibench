import os
import httpx
from identity_models import RefreshRequest, RefreshResponse, normalize_refresh_response


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")


def refresh_session(refresh_token, audience=None, scope=None):
    req = RefreshRequest(
        refresh_token=refresh_token,
        client_id=AUTH0_CLIENT_ID,
        audience=audience or "https://{}/userinfo".format(AUTH0_DOMAIN),
        scope=scope,
    )
    url = "https://{}/oauth/token".format(AUTH0_DOMAIN)
    body = {
        "grant_type": "refresh_token",
        "client_id": req.client_id,
        "refresh_token": req.refresh_token,
    }
    if req.audience:
        body["audience"] = req.audience
    if req.scope:
        body["scope"] = req.scope
    resp = httpx.post(url, json=body)
    resp.raise_for_status()
    return normalize_refresh_response(resp.json())
