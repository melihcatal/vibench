# register_user.py
# Create a new email/password user account (same-scenario integration)

import os
import json
from identity_client import init, decode_jwt
from identity_models import (
    CreateUserRequest,
    CreateUserResponse,
    normalize_create_user_payload,
)

# Choose a concrete provider and import its SDK / REST client
# Example: Firebase Authentication
if os.getenv("PROVIDER", "Firebase") == "Firebase":
    import firebase_admin
    from firebase_admin import auth

# Initialize provider client
init()


def create_user(payload: CreateUserRequest) -> CreateUserResponse:
    """
    Create a new local email/password account using the configured provider.
    Returns a normalized CreateUserResponse containing at least user_id and email.
    """
    # Convert to provider-specific format
    provider_data = normalize_create_user_payload(payload)

    # Firebase example: create_user accepts email/password directly
    try:
        user_record = auth.create_user(**provider_data)
    except Exception as exc:
        raise RuntimeError(f"Failed to create user: {exc}")

    user_id = user_record.uid
    email = user_record.email
    created_at = int(user_record.user_metadata.creation_time)

    return CreateUserResponse(user_id=user_id, email=email, created_at=created_at)


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     resp = create_user(CreateUserRequest(email="alice@example.com", password="Secret123!", display_name="Alice"))
#     print(json.dumps(resp, indent=2))
