"""
Refresh an expired session or access token using Firebase Authentication
token refresh endpoint.

Provider: Firebase Auth (Identity Toolkit securetoken API)
Concrete provider signals: securetoken.googleapis.com, identitytoolkit.googleapis.com,
                           firebase_admin.auth, FIREBASE_PROJECT_ID.
"""

import logging
from typing import Optional, Dict, Any

import requests
import firebase_admin.auth

from identity_client import (
    initialize_firebase_app,
    get_firebase_auth_client,
    verify_id_token,
    FIREBASE_PROJECT_ID,
)
from identity_models import (
    RefreshTokenRequest,
    SessionTokens,
)


logger = logging.getLogger(__name__)

# Firebase securetoken endpoint for token refresh
FIREBASE_SECURETOKEN_ENDPOINT = "https://securetoken.googleapis.com/v1/token"


def refresh_access_token(
    request: RefreshTokenRequest,
) -> Dict[str, Any]:
    """
    Refresh an expired Firebase access token using the refresh token.
    
    Calls the concrete Firebase securetoken API:
    https://securetoken.googleapis.com/v1/token
    
    This endpoint exchanges a valid refresh_token for a new id_token,
    new refresh_token, and updated expires_in value.
    
    Args:
        request: RefreshTokenRequest containing the current refresh_token.
        
    Returns:
        Dict with new tokens or error information.
    """
    payload = request.to_firebase_payload()
    
    try:
        response = requests.post(
            FIREBASE_SECURETOKEN_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15,
        )
        response.raise_for_status()
        response_data = response.json()
        
        session_tokens = SessionTokens(
            id_token=response_data.get("id_token", ""),
            refresh_token=response_data.get("refresh_token", request.refresh_token),
            expires_in=int(response_data.get("expires_in", 3600)),
            token_type=response_data.get("token_type", "Bearer"),
            user_id=response_data.get("user_id"),
        )
        
        logger.info(
            "Firebase securetoken refresh success: uid=%s, expires_in=%d (API: securetoken.googleapis.com)",
            session_tokens.user_id,
            session_tokens.expires_in,
        )
        
        return {
            "success": True,
            "tokens": session_tokens.to_dict(),
            "provider": "firebase_auth",
            "api_endpoint": "securetoken.googleapis.com",
        }
        
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json() if e.response else {}
        firebase_error = error_data.get("error", "")
        
        logger.warning(
            "Firebase securetoken refresh failed: %s",
            firebase_error,
        )
        
        return {
            "success": False,
            "error": firebase_error or "REFRESH_FAILED",
            "message": error_data.get("error_description", "Token refresh failed"),
            "provider": "firebase_auth",
        }
    except requests.exceptions.RequestException as e:
        logger.error("Firebase securetoken network error: %s", str(e))
        return {
            "success": False,
            "error": "NETWORK_ERROR",
            "message": str(e),
            "provider": "firebase_auth",
        }


def revoke_refresh_tokens(
    uid: str,
    app=None,
) -> Dict[str, Any]:
    """
    Revoke all refresh tokens for a Firebase user.
    
    Uses firebase_admin.auth.revoke_refresh_tokens which invalidates
    all existing sessions for the user via the Firebase Auth backend.
    
    Args:
        uid: The Firebase user UID whose tokens should be revoked.
        app: Optional Firebase app instance.
        
    Returns:
        Dict indicating success or failure.
    """
    target_app = app or initialize_firebase_app()
    auth_client = firebase_admin.auth.client(target_app)
    
    try:
        auth_client.revoke_refresh_tokens(uid)
        
        logger.info(
            "Firebase Auth refresh tokens revoked for uid=%s (project: %s)",
            uid,
            target_app.project_id,
        )
        
        return {
            "success": True,
            "uid": uid,
            "message": "All refresh tokens have been revoked.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.UserNotFoundError:
        logger.warning("Firebase Auth user not found: uid=%s", uid)
        return {
            "success": False,
            "error": "USER_NOT_FOUND",
            "message": f"No user found with uid {uid}.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.FirebaseError as e:
        logger.error("Firebase Auth revoke error: %s", str(e))
        return {
            "success": False,
            "error": "FIREBASE_ERROR",
            "message": str(e),
            "provider": "firebase_auth",
        }


def check_session_validity(
    id_token: str,
    check_revoked: bool = True,
) -> Dict[str, Any]:
    """
    Check if a Firebase ID token is still valid and not revoked.
    
    Uses firebase_admin.auth.verify_id_token which validates the token
    against Firebase's public key infrastructure.
    
    Args:
        id_token: The Firebase ID token to validate.
        check_revoked: Whether to check revocation status.
        
    Returns:
        Dict with validity status and decoded claims.
    """
    try:
        app = initialize_firebase_app()
        decoded = verify_id_token(id_token, app=app, check_revoked=check_revoked)
        
        return {
            "success": True,
            "valid": True,
            "claims": decoded,
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.ExpiredIdTokenError:
        return {
            "success": False,
            "valid": False,
            "error": "TOKEN_EXPIRED",
            "message": "The ID token has expired. Please refresh.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.RevokedIdTokenError:
        return {
            "success": False,
            "valid": False,
            "error": "TOKEN_REVOKED",
            "message": "The ID token has been revoked.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.InvalidIdTokenError:
        return {
            "success": False,
            "valid": False,
            "error": "INVALID_TOKEN",
            "message": "The ID token is invalid.",
            "provider": "firebase_auth",
        }
