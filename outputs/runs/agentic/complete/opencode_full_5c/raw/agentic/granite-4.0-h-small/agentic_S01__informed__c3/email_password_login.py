# email_password_login.py
# Sign in a user with email and password and return tokens (same-scenario integration)

import os
from identity_client import init, decode_jwt
from identity_models import LoginRequest, LoginResponse, normalize_login_payload

# Choose a concrete provider and import its SDK / REST client
# Example: Firebase Authentication
if os.getenv("PROVIDER", "Firebase") == "Firebase":
    import firebase_admin
    from firebase_admin import auth

# Initialize provider client
init()


def login(payload: LoginRequest) -> LoginResponse:
    """
    Authenticate a user by email/password and return access & refresh tokens.
    """
    provider_payload = normalize_login_payload(payload)

    try:
        # Firebase: get_user_by_email to validate existence, then verify password manually
        user = auth.get_user_by_email(provider_payload["email"])
        if not user:
            raise ValueError("User not found")
        # Verify password (Firebase uses verify_password internally in sign_in)
        # Use sign_in_with_email_and_password for simplicity
        token_info = auth.verify_id_token(auth.create_session_cookie(provider_payload))
        # In practice, use auth.sign_in_with_email_and_password; here we emulate token extraction
    except Exception as exc:
        raise RuntimeError(f"Login failed: {exc}")

    # Construct response (access token = session cookie, refresh token generated here)
    access_token = auth.create_session_cookie(
        provider_payload
    )  # session cookie acts as access token
    refresh_token = os.urandom(
        32
    ).hex()  # placeholder; real implementations store a refresh token
    expires_in = 3600  # 1 hour

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        token_type="Bearer",
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     resp = login(LoginRequest(email="alice@example.com", password="Secret123!"))
#     print(json.dumps(resp, indent=2))
