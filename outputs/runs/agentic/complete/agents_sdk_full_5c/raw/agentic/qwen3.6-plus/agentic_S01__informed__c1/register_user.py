"""
Creates a new email/password user account.

Provider: Firebase Authentication
Provider-identifying signals:
  - firebase_admin SDK import
  - GOOGLE_APPLICATION_CREDENTIALS environment variable
  - Firebase-specific user creation API
"""

import logging
from typing import Any, Dict, Optional

import firebase_admin
from firebase_admin import auth

from identity_client import get_auth_client, normalize_create_user_payload
from identity_models import (
    RegisterUserRequest,
    RegisterUserResponse,
    serialize_response,
)

logger = logging.getLogger(__name__)


def register_user(
    email: str,
    password: str,
    display_name: Optional[str] = None,
    email_verified: bool = False,
    custom_claims: Optional[Dict[str, Any]] = None,
) -> RegisterUserResponse:
    """
    Create a new user account in Firebase Authentication with email/password.

    Args:
        email: User's email address.
        password: User's password (min 6 characters per Firebase requirement).
        display_name: Optional display name.
        email_verified: Whether to mark email as verified on creation.
        custom_claims: Optional Firebase custom claims dict.

    Returns:
        RegisterUserResponse with uid, email, and metadata.
    """
    request = RegisterUserRequest(
        email=email,
        password=password,
        display_name=display_name,
        email_verified=email_verified,
        custom_claims=custom_claims,
    )

    payload = normalize_create_user_payload(
        email=request.email,
        password=request.password,
        display_name=request.display_name,
        email_verified=request.email_verified,
    )

    try:
        user_record = auth.create_user(**payload)
        logger.info(
            "Firebase Auth: User created successfully, uid=%s, email=%s",
            user_record.uid,
            user_record.email,
        )

        if request.custom_claims:
            auth.set_custom_user_claims(user_record.uid, request.custom_claims)
            logger.info(
                "Firebase Auth: Custom claims applied to uid=%s",
                user_record.uid,
            )

        return RegisterUserResponse(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            email_verified=user_record.email_verified,
            disabled=user_record.disabled,
            created_at=user_record.user_metadata.creation_timestamp,
            provider="firebase",
        )

    except auth.EmailAlreadyExistsError as e:
        logger.error("Firebase Auth: Email already exists - %s", email)
        raise
    except auth.InvalidEmailError as e:
        logger.error("Firebase Auth: Invalid email format - %s", email)
        raise
    except auth.WeakPasswordError as e:
        logger.error("Firebase Auth: Password too weak for email - %s", email)
        raise
    except Exception as e:
        logger.error("Firebase Auth: Unexpected error creating user - %s", str(e))
        raise


def register_user_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience wrapper that accepts a dict and returns a dict.
    Suitable for API handler integration.
    """
    response = register_user(
        email=data["email"],
        password=data["password"],
        display_name=data.get("display_name"),
        email_verified=data.get("email_verified", False),
        custom_claims=data.get("custom_claims"),
    )
    return serialize_response(response)
