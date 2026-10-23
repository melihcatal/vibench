"""
Register a new email/password user account using Firebase Authentication Admin SDK.

This module uses firebase-admin (Google Cloud / Firebase Auth) to create a new
user record in the Firebase project. The provider-identifying signals include:
  - firebase_admin / firebase_admin.auth SDK imports
  - FirebaseAuthClient usage
  - Firebase project / GOOGLE_APPLICATION_CREDENTIALS configuration
  - Firebase-specific UserRecord response
"""

from __future__ import annotations

from typing import Optional

from identity_models import RegisterUserRequest, RegisterUserResponse
from identity_client import create_firebase_user


def register_user(
    email: str,
    password: str,
    display_name: Optional[str] = None,
    locale: Optional[str] = "en-US",
    metadata: Optional[dict] = None,
) -> RegisterUserResponse:
    """
    Create a new email/password user in Firebase Auth.

    Args:
        email: The user's email address.
        password: The user's password (min 6 characters for Firebase).
        display_name: Optional display name.
        locale: Optional locale for the user.
        metadata: Optional key-value metadata stored as custom claims.

    Returns:
        RegisterUserResponse with uid, email, display_name, and created_at.
    """
    request = RegisterUserRequest(
        email=email,
        password=password,
        display_name=display_name,
        locale=locale,
        metadata=metadata,
    )

    custom_claims = None
    if request.metadata:
        custom_claims = dict(request.metadata)
    if request.locale:
        custom_claims = custom_claims or {}
        custom_claims["locale"] = request.locale

    user_record = create_firebase_user(
        email=request.email,
        password=request.password,
        display_name=request.display_name,
        custom_claims=custom_claims,
    )

    response = RegisterUserResponse.from_firebase_user_record(user_record)
    return response


if __name__ == "__main__":
    import os, sys
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")
    os.environ.setdefault("FIREBASE_PROJECT_ID", "demo-project")
    os.environ.setdefault("FIREBASE_WEB_API_KEY", "demo-api-key")

    result = register_user(
        email="newuser@example.com",
        password="SecureP@ss123",
        display_name="New User",
        locale="en-US",
    )
    print(result.model_dump_json(indent=2))
