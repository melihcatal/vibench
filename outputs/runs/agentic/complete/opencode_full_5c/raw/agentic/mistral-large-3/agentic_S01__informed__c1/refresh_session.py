from typing import Dict, Any
import os
from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError
from identity_models import (
    RefreshSessionRequest,
    RefreshSessionResponse,
    normalize_firebase_error,
)

# Initialize Firebase Admin SDK with provider-specific credentials
if not auth._apps:
    initialize_app(options={"projectId": os.getenv("FIREBASE_PROJECT_ID")})


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    """
    Refreshes an expired session or access token using Firebase Authentication.
    """
    try:
        # Verify the refresh token and generate a new custom token
        decoded_token = auth.verify_id_token(request.refresh_token)
        new_custom_token = auth.create_custom_token(decoded_token["uid"])
        return RefreshSessionResponse(
            success=True, access_token=new_custom_token, expires_in=3600
        )
    except FirebaseError as e:
        return RefreshSessionResponse(success=False, error=normalize_firebase_error(e))
