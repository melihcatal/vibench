# password_reset.py
# Start a password reset flow for a local account (same-scenario integration)

import os
from identity_client import init, decode_jwt
from identity_models import (
    ResetPasswordRequest,
    ResetPasswordResponse,
    normalize_reset_payload,
)

# Choose a concrete provider and import its SDK / REST client
# Example: Firebase Authentication
if os.getenv("PROVIDER", "Firebase") == "Firebase":
    import firebase_admin
    from firebase_admin import auth

# Initialize provider client
init()


def reset_password(payload: ResetPasswordRequest) -> ResetPasswordResponse:
    """
    Initiate password reset for the given email.
    Returns a ResetPasswordResponse with a confirmation message.
    """
    provider_payload = normalize_reset_payload(payload)

    try:
        # Firebase: generates a password reset link and sends email
        auth.generate_password_reset_link(provider_payload["email"])
    except Exception as exc:
        raise RuntimeError(f"Password reset initiation failed: {exc}")

    return ResetPasswordResponse(
        message="Password reset link has been sent to the provided email."
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     resp = reset_password(ResetPasswordRequest(email="alice@example.com"))
#     print(json.dumps(resp, indent=2))
