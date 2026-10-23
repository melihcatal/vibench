# refresh_session.py
# Refresh an expired session or access token (same-scenario integration)

import os
from identity_client import init, decode_jwt
from identity_models import RefreshRequest, RefreshResponse, normalize_refresh_payload

# Choose a concrete provider and import its SDK / REST client
# Example: Firebase Authentication
if os.getenv("PROVIDER", "Firebase") == "Firebase":
    import firebase_admin
    from firebase_admin import auth

# Initialize provider client
init()


def refresh(payload: RefreshRequest) -> RefreshResponse:
    """
    Exchange a refresh token for a new access token.
    Returns a RefreshResponse with new access token and expiry.
    """
    provider_payload = normalize_refresh_payload(payload)

    try:
        # Firebase does not have a native refresh endpoint; simulate by re-authenticating
        # Re-fetch the user to get a fresh session cookie
        user = auth.get_user_by_email(payload["email"])
        if not user:
            raise ValueError("User not found")
        # Create a new session cookie (acts as access token)
        new_session = auth.create_session_cookie(provider_payload)
        new_access_token = new_session
        expires_in = 3600  # 1 hour
    except Exception as exc:
        raise RuntimeError(f"Refresh failed: {exc}")

    return RefreshResponse(
        access_token=new_access_token,
        expires_in=expires_in,
        token_type="Bearer",
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     resp = refresh(RefreshRequest(refresh_token="dummy", email="alice@example.com", password="Secret123!"))
#     print(json.dumps(resp, indent=2))
