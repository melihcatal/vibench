import os
from firebase_admin import auth
from identity_client import initialize_firebase
from identity_models import RefreshSessionRequest, RefreshSessionResponse

# Initialize Firebase Admin SDK (if not already initialized)
initialize_firebase()


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    """Verifies the validity of an existing Firebase ID token.
    Firebase Admin SDK is primarily for server-side verification and management.
    Clients typically use Firebase Client SDKs to refresh ID tokens using refresh tokens.
    """
    try:
        # Verify the ID token. This will raise an exception if the token is invalid or expired.
        decoded_token = auth.verify_id_token(request.id_token)
        # If verification succeeds, the session is considered valid.
        return RefreshSessionResponse(is_valid=True)
    except auth.InvalidIdTokenError as e:
        return RefreshSessionResponse(is_valid=False)  # Token is invalid or expired
    except Exception as e:
        raise ValueError(f"Error verifying ID token: {e}")
