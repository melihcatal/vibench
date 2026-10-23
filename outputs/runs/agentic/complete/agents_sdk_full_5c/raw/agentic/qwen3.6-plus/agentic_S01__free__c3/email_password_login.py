"""
Sign in a user with email and password using Firebase Authentication
and return ID and refresh tokens.

Provider: Firebase Auth (Identity Toolkit REST API + Admin SDK)
Concrete provider signals: identitytoolkit.googleapis.com, firebase-admin,
                           FIREBASE_PROJECT_ID, accounts:signInWithPassword.
"""

import logging
import base64
import json
from typing import Optional, Dict, Any

import requests

from identity_client import (
    initialize_firebase_app,
    get_firebase_rest_url,
    verify_id_token,
    FIREBASE_WEB_API_KEY,
)
from identity_models import (
    LoginRequest,
    SessionTokens,
    UserProfile,
)


logger = logging.getLogger(__name__)

# Firebase Identity Toolkit endpoint for email/password sign-in
FIREBASE_SIGNIN_ENDPOINT = "accounts:signInWithPassword"


def login_with_email_password(
    request: LoginRequest,
) -> Dict[str, Any]:
    """
    Authenticate a user with email/password via Firebase Identity Toolkit REST API.
    
    Calls the concrete Firebase endpoint:
    https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword
    
    Args:
        request: LoginRequest with email and password.
        
    Returns:
        Dict with id_token, refresh_token, expires_in, and user profile.
    """
    signin_url = get_firebase_rest_url(FIREBASE_SIGNIN_ENDPOINT)
    payload = request.to_firebase_payload()
    
    try:
        response = requests.post(signin_url, json=payload, timeout=15)
        response.raise_for_status()
        response_data = response.json()
        
        session_tokens = SessionTokens.from_firebase_rest(response_data)
        
        logger.info(
            "Firebase Identity Toolkit login success: uid=%s, email=%s",
            session_tokens.user_id,
            session_tokens.email,
        )
        
        decoded_claims = _decode_id_token_claims(session_tokens.id_token)
        
        user_profile = UserProfile(
            uid=session_tokens.user_id or "",
            email=session_tokens.email or "",
            display_name=decoded_claims.get("name"),
            locale=decoded_claims.get("locale", "en"),
            onboarding_completed=decoded_claims.get("onboarding_completed", False),
        )
        
        return {
            "success": True,
            "tokens": session_tokens.to_dict(),
            "user": user_profile.to_dict(),
            "provider": "firebase_auth",
            "api_endpoint": "identitytoolkit.googleapis.com",
        }
        
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json() if e.response else {}
        firebase_error = error_data.get("error", {}).get("message", str(e))
        
        error_map = {
            "EMAIL_NOT_FOUND": "No account found with this email.",
            "INVALID_PASSWORD": "Incorrect password.",
            "USER_DISABLED": "This account has been disabled.",
        }
        
        user_friendly = error_map.get(firebase_error, firebase_error)
        
        logger.warning(
            "Firebase Identity Toolkit login failed: %s (email=%s)",
            firebase_error,
            request.email,
        )
        
        return {
            "success": False,
            "error": firebase_error,
            "message": user_friendly,
            "provider": "firebase_auth",
        }
    except requests.exceptions.RequestException as e:
        logger.error("Firebase Identity Toolkit network error: %s", str(e))
        return {
            "success": False,
            "error": "NETWORK_ERROR",
            "message": str(e),
            "provider": "firebase_auth",
        }


def validate_session_and_get_claims(
    id_token: str,
    check_revoked: bool = True,
) -> Dict[str, Any]:
    """
    Validate a Firebase ID token and return decoded claims.
    
    Uses firebase_admin.auth.verify_id_token which communicates with
    https://www.googleapis.com/robot/v1/metadata/x509/... for key verification.
    
    Args:
        id_token: The Firebase ID token to validate.
        check_revoked: Whether to check if the token has been revoked.
        
    Returns:
        Dict with decoded claims or error information.
    """
    try:
        app = initialize_firebase_app()
        decoded_token = verify_id_token(id_token, app=app, check_revoked=check_revoked)
        
        logger.info(
            "Firebase ID token validated: uid=%s (project: %s)",
            decoded_token.get("uid"),
            app.project_id,
        )
        
        return {
            "success": True,
            "claims": decoded_token,
            "provider": "firebase_auth",
        }
    except Exception as e:
        logger.error("Firebase ID token validation failed: %s", str(e))
        return {
            "success": False,
            "error": "INVALID_TOKEN",
            "message": str(e),
            "provider": "firebase_auth",
        }


def _decode_id_token_claims(id_token: str) -> Dict[str, Any]:
    """
    Decode the JWT payload from a Firebase ID token (without signature verification).
    Used for extracting user display name and locale from token claims.
    """
    try:
        parts = id_token.split(".")
        if len(parts) != 3:
            return {}
        payload_bytes = base64.urlsafe_b64decode(parts[1] + "==")
        return json.loads(payload_bytes)
    except Exception:
        return {}
