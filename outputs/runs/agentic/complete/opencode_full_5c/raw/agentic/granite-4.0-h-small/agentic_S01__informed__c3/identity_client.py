# identity_client.py
# Local configuration and client helper utilities for Email/Password Account Lifecycle

import os
import json

# Select a concrete provider (example: Firebase Authentication)
PROVIDER = "Firebase"

# Provider-specific credentials
if PROVIDER == "Firebase":
    # GOOGLE_APPLICATION_CREDENTIALS should point to service account JSON
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "service_account.json"
    )

    try:
        import firebase_admin
        from firebase_admin import auth
    except Exception as e:
        raise ImportError(
            "Firebase Admin SDK not installed. Run pip install firebase-admin"
        ) from e

    def init():
        # Ensure App is initialized
        if not firebase_admin._apps:
            firebase_admin.initialize_app()

    def decode_jwt(token):
        # Wrapper around firebase auth verify_id_token
        id_token = auth.verify_id_token(token)
        return id_token

else:
    raise ValueError(f"Unsupported provider: {PROVIDER}")
