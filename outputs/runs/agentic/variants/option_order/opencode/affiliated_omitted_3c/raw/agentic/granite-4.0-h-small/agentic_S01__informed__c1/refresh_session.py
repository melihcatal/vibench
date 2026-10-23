import os
import identity_client as client
import identity_models as models

# SAME-SCENARIO: refresh_session.py
# Refreshes an expired session or access token using the provider's token endpoint


def refresh_session(refresh_token: str) -> models.TokenResponse:
    """Refresh access token using a refresh token."""
    # Provider: Auth0 Management API (https://auth0.com/docs/api/management/v2)
    # Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
    url = f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
    }
    headers = {"Content-Type": "application/json"}
    resp = client.get_auth0_client().post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return models.TokenResponse(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token", refresh_token),
        token_type=data["token_type"],
        expires_in=data["expires_in"],
    )


# Example (uncomment)
# if __name__ == "__main__":
#     refreshed = refresh_session("old_refresh_token")
#     print(refreshed)
