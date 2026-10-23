"""
Create a new email/password user account using Firebase Authentication.

Provider: Firebase Auth (firebase-admin SDK + Identity Toolkit REST API)
Concrete provider signals: firebase_admin.auth, identitytoolkit.googleapis.com,
                           FIREBASE_PROJECT_ID environment variable.
"""

import logging
from typing import Optional, Dict, Any

import firebase_admin.auth

from identity_client import (
    initialize_firebase_app,
    get_firebase_auth_client,
    get_firebase_rest_url,
    FIREBASE_WEB_API_KEY,
)
from identity_models import (
    RegisterUserRequest,
    UserResponse,
    SessionTokens,
)


logger = logging.getLogger(__name__)

# Firebase Identity Toolkit endpoint for email/password signup
FIREBASE_SIGNUP_ENDPOINT = "accounts:signUp"


def register_user(
    request: RegisterUserRequest,
    app=None,
) -> Dict[str, Any]:
    """
    Register a new user with email and password via Firebase Auth Admin SDK.
    
    Uses firebase_admin.auth.create_user which targets the
    https://identitytoolkit.googleapis.com API for Firebase Auth.
    
    Args:
        request: RegisterUserRequest with email, password, and optional profile fields.
        app: Optional Firebase app instance.
        
    Returns:
        Dict with uid, email, display_name, and other user fields.
    """
    target_app = app or initialize_firebase_app()
    auth_client = firebase_admin.auth.client(target_app)
    
    payload = request.to_firebase_payload()
    
    try:
        user_record = auth_client.create_user(**payload)
        logger.info(
            "Firebase Auth user created: uid=%s, email=%s (project: %s)",
            user_record.uid,
            user_record.email,
            target_app.project_id,
        )
        
        user_response = UserResponse.from_firebase_user(user_record)
        
        return {
            "success": True,
            "user": user_response.to_dict(),
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.EmailAlreadyExistsError:
        logger.warning("Firebase Auth email already exists: %s", request.email)
        return {
            "success": False,
            "error": "EMAIL_ALREADY_EXISTS",
            "message": f"An account with email {request.email} already exists.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.InvalidEmailError:
        logger.warning("Firebase Auth invalid email: %s", request.email)
        return {
            "success": False,
            "error": "INVALID_EMAIL",
            "message": "The email address is not valid.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.WeakPasswordError:
        logger.warning("Firebase Auth weak password for email: %s", request.email)
        return {
            "success": False,
            "error": "WEAK_PASSWORD",
            "message": "The password is too weak.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.FirebaseError as e:
        logger.error("Firebase Auth registration error: %s", str(e))
        return {
            "success": False,
            "error": "FIREBASE_ERROR",
            "message": str(e),
            "provider": "firebase_auth",
        }


def register_user_with_web_signup(
    request: RegisterUserRequest,
    http_client=None,
) -> Dict[str, Any]:
    """
    Register a user via the Firebase Identity Toolkit REST API endpoint.
    
    This uses the concrete Firebase endpoint:
    https://identitytoolkit.googleapis.com/v1/accounts:signUp
    
    Args:
        request: RegisterUserRequest with email and password.
        http_client: Optional HTTP client (uses requests if None).
        
    Returns:
        Dict with success status, user data, and session tokens.
    """
    import requests
    
    signup_url = get_firebase_rest_url(FIREBASE_SIGNUP_ENDPOINT)
    payload = request.to_web_signup_payload()
    
    try:
        response = requests.post(signup_url, json=payload, timeout=15)
        response.raise_for_status()
        response_data = response.json()
        
        session_tokens = SessionTokens.from_firebase_rest(response_data)
        
        logger.info(
            "Firebase Identity Toolkit signup success: uid=%s (API: identitytoolkit.googleapis.com)",
            response_data.get("localId"),
        )
        
        return {
            "success": True,
            "tokens": session_tokens.to_dict(),
            "provider": "firebase_auth",
            "api_endpoint": "identitytoolkit.googleapis.com",
        }
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json() if e.response else {}
        error_msg = error_data.get("error", {}).get("message", str(e))
        logger.error("Firebase Identity Toolkit signup failed: %s", error_msg)
        return {
            "success": False,
            "error": error_msg,
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
