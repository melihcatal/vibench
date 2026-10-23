import os
import urllib.parse
from identity_client import IdentityClient


def oauth_callback(request):
    """Handles the OAuth/OIDC callback and exchanges the authorization code for tokens.
    Uses Alibaba Cloud IDaaS EIAM OIDC as the concrete provider.
    Expects the request object to contain either query parameters or POST body with 'code' and 'state'.
    Returns a dict with 'access_token', 'id_token', and 'refresh_token' on success.
    """
    code = request.get("GET", {}).get("code")
    state = request.get("GET", {}).get("state")
    # Fallback to form-encoded body if code is missing (e.g., Flask request.form)
    if not code:
        code = request.get("form", {}).get("code")
        state = request.get("form", {}).get("state")
    client = IdentityClient()
    # PKCE verification (client_secret not required for public client)
    client.verify_pkce_challenge(request.get("code_verifier"))

    # Exchange code: Alibaba IDaaS EIAM OIDC token endpoint
    token_resp = client.exchange_code_for_token(code)
    if not token_resp.ok:
        raise RuntimeError(f"Token exchange failed: {token_resp.text}")

    data = token_resp.json()
    return {
        "access_token": data.get("access_token"),
        "id_token": data.get("id_token"),
        "refresh_token": data.get("refresh_token"),
    }


if __name__ == "__main__":
    # Example using a mock request (replace with your web framework)
    mock_request = {
        "GET": {"code": "mock_code", "state": "mock_state"},
        "form": {},
        "headers": {},
    }
    print(oauth_callback(mock_request))
