"""
Start a password reset flow for a local email/password account using
Firebase Authentication out-of-band (OOB) code generation.

Provider: Firebase Auth (Identity Toolkit oobCode API)
Concrete provider signals: identitytoolkit.googleapis.com, firebase_admin.auth,
                           FIREBASE_PROJECT_ID, accounts:sendOobCode.
"""

import logging
from typing import Optional, Dict, Any

import requests
import firebase_admin.auth

from identity_client import (
    initialize_firebase_app,
    get_firebase_rest_url,
    get_firebase_auth_client,
    FIREBASE_WEB_API_KEY,
)
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
)


logger = logging.getLogger(__name__)

# Firebase Identity Toolkit endpoint for sending OOB codes
FIREBASE_OOB_ENDPOINT = "accounts:sendOobCode"


def initiate_password_reset(
    request: PasswordResetRequest,
) -> Dict[str, Any]:
    """
    Initiate a password reset by sending an email with a reset link.
    
    Calls the concrete Firebase Identity Toolkit endpoint:
    https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode
    
    The requestType PASSWORD_RESET generates an oobCode that can be used
    to construct a password reset URL.
    
    Args:
        request: PasswordResetRequest with email and optional continue_url.
        
    Returns:
        Dict with email, oob_code, and reset link if applicable.
    """
    oob_url = get_firebase_rest_url(FIREBASE_OOB_ENDPOINT)
    payload = request.to_firebase_payload()
    
    try:
        response = requests.post(oob_url, json=payload, timeout=15)
        response.raise_for_status()
        response_data = response.json()
        
        reset_response = PasswordResetResponse.from_firebase_response(response_data)
        
        logger.info(
            "Firebase Identity Toolkit password reset initiated: email=%s, oobCode=%s",
            reset_response.email,
            reset_response.oob_code[:10] + "..." if reset_response.oob_code else "N/A",
        )
        
        return {
            "success": True,
            "reset": reset_response.to_dict(),
            "provider": "firebase_auth",
            "api_endpoint": "identitytoolkit.googleapis.com",
        }
        
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json() if e.response else {}
        firebase_error = error_data.get("error", {}).get("message", str(e))
        
        logger.warning(
            "Firebase Identity Toolkit password reset failed: %s (email=%s)",
            firebase_error,
            request.email,
        )
        
        return {
            "success": False,
            "error": firebase_error,
            "message": _map_firebase_error(firebase_error),
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


def generate_password_reset_link(
    email: str,
    continue_url: Optional[str] = None,
    app=None,
) -> Dict[str, Any]:
    """
    Generate a password reset link using the Firebase Admin SDK.
    
    Uses firebase_admin.auth.generate_password_reset_link which internally
    calls the Firebase Auth backend to create a reset link.
    
    Args:
        email: The user's email address.
        continue_url: Optional URL to redirect to after reset.
        app: Optional Firebase app instance.
        
    Returns:
        Dict with the generated password reset link.
    """
    target_app = app or initialize_firebase_app()
    auth_client = firebase_admin.auth.client(target_app)
    
    action_code_settings = firebase_admin.auth.ActionCodeSettings(
        url=continue_url or "https://example.com/reset-complete",
        handle_code_in_app=False,
    )
    
    try:
        reset_link = auth_client.generate_password_reset_link(
            email=email,
            action_code_settings=action_code_settings,
        )
        
        logger.info(
            "Firebase Admin SDK password reset link generated: email=%s (project: %s)",
            email,
            target_app.project_id,
        )
        
        return {
            "success": True,
            "reset_link": reset_link,
            "email": email,
            "provider": "firebase_auth",
        }
        
    except firebase_admin.auth.UserNotFoundError:
        logger.warning("Firebase Auth user not found for password reset: %s", email)
        return {
            "success": False,
            "error": "USER_NOT_FOUND",
            "message": f"No account found with email {email}.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.InvalidEmailError:
        logger.warning("Firebase Auth invalid email for password reset: %s", email)
        return {
            "success": False,
            "error": "INVALID_EMAIL",
            "message": "The email address is not valid.",
            "provider": "firebase_auth",
        }
    except firebase_admin.auth.FirebaseError as e:
        logger.error("Firebase Admin SDK password reset error: %s", str(e))
        return {
            "success": False,
            "error": "FIREBASE_ERROR",
            "message": str(e),
            "provider": "firebase_auth",
        }


def complete_password_reset(
    oob_code: str,
    new_password: str,
) -> Dict[str, Any]:
    """
    Complete a password reset using the OOB code from the reset email.
    
    Calls the Firebase Identity Toolkit confirmResetPassword endpoint.
    
    Args:
        oob_code: The out-of-band code from the reset email.
        new_password: The new password to set.
        
    Returns:
        Dict indicating success or failure.
    """
    confirm_url = get_firebase_rest_url("accounts:resetPassword")
    payload = {
        "oobCode": oob_code,
        "newPassword": new_password,
    }
    
    try:
        response = requests.post(confirm_url, json=payload, timeout=15)
        response.raise_for_status()
        response_data = response.json()
        
        logger.info(
            "Firebase Identity Toolkit password reset completed: email=%s",
            response_data.get("email", "unknown"),
        )
        
        return {
            "success": True,
            "email": response_data.get("email", ""),
            "message": "Password has been reset successfully.",
            "provider": "firebase_auth",
        }
        
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json() if e.response else {}
        firebase_error = error_data.get("error", {}).get("message", str(e))
        
        return {
            "success": False,
            "error": firebase_error,
            "message": _map_firebase_error(firebase_error),
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


def _map_firebase_error(error_code: str) -> str:
    """Map Firebase error codes to user-friendly messages."""
    error_map = {
        "EMAIL_NOT_FOUND": "No account exists with this email address.",
        "INVALID_EMAIL": "The email address is not valid.",
        "WEAK_PASSWORD": "The password is too weak. Please choose a stronger password.",
        "INVALID_OOB_CODE": "The password reset link has expired or is invalid.",
        "EXPIRED_OOB_CODE": "The password reset link has expired.",
        "INVALID_ACTION_CODE": "The action code is invalid.",
        "TOO_MANY_ATTEMPTS": "Too many attempts. Please try again later.",
    }
    return error_map.get(error_code, "An error occurred. Please try again.")
