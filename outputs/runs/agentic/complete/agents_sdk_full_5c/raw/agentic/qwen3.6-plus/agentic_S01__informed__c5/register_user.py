"""
register_user.py
Creates a new email/password user account via Firebase Authentication.

Provider: Firebase Authentication (firebase-admin SDK)
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import os
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from identity_client import get_firebase_app
from identity_models import RegistrationRequest, RegistrationResponse


def create_firebase_app() -> firebase_admin.App:
    """Initialize or retrieve the Firebase Admin SDK app instance."""
    return get_firebase_app()


def register_user(request: RegistrationRequest) -> RegistrationResponse:
    """
    Creates a new email/password user account in Firebase Authentication.

    Args:
        request: RegistrationRequest containing email, password, and display_name.

    Returns:
        RegistrationResponse with uid, email, and display_name of the created user.
    """
    app = create_firebase_app()

    user_record = firebase_auth.create_user(
        email=request.email,
        password=request.password,
        display_name=request.display_name,
        email_verified=False,
        app=app,
    )

    return RegistrationResponse(
        uid=user_record.uid,
        email=user_record.email,
        display_name=user_record.display_name,
        email_verified=user_record.email_verified,
        created_at=user_record.user_metadata.creation_timestamp,
    )


if __name__ == "__main__":
    req = RegistrationRequest(
        email="newuser@example.com",
        password="SecureP@ssw0rd!",
        display_name="New User",
    )
    response = register_user(req)
    print(f"Registered user: {response.uid} ({response.email})")
