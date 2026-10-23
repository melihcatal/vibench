"""
Local configuration and client helper utilities for Email/Password Account Lifecycle.

Provider: Firebase Authentication
Provider-identifying signals:
  - GOOGLE_APPLICATION_CREDENTIALS env var
  - firebase_admin SDK import
  - Firebase project configuration
"""

import os
from typing import Any, Dict, Optional

import firebase_admin
from firebase_admin import auth, credentials


FIREBASE_PROJECT_ID_ENV = "FIREBASE_PROJECT_ID"
GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


def _ensure_firebase_app() -> firebase_admin.App:
    """Initialize Firebase app if not already initialized."""
    if firebase_admin._apps:
        return list(firebase_admin._apps.values())[0]

    creds_path = os.environ.get(GOOGLE_APPLICATION_CREDENTIALS_ENV)
    project_id = os.environ.get(FIREBASE_PROJECT_ID_ENV)

    if creds_path and os.path.isfile(creds_path):
        cred = credentials.Certificate(creds_path)
    else:
        cred = credentials.ApplicationDefault()

    app_options: Dict[str, Any] = {}
    if project_id:
        app_options["projectId"] = project_id

    return firebase_admin.initialize_app(cred, app_options)


def get_auth_client() -> auth.Client:
    """Return a Firebase Auth client for user management operations."""
    app = _ensure_firebase_app()
    return auth.client.AuthClient(app)


def normalize_create_user_payload(
    email: str,
    password: str,
    display_name: Optional[str] = None,
    email_verified: bool = False,
) -> Dict[str, Any]:
    """
    Normalize input fields into a payload compatible with
    firebase_admin.auth.create_user().
    """
    payload: Dict[str, Any] = {
        "email": email,
        "password": password,
        "email_verified": email_verified,
    }
    if display_name:
        payload["display_name"] = display_name
    return payload


def normalize_login_response(user_record: auth.UserRecord) -> Dict[str, Any]:
    """Normalize a Firebase UserRecord into a standard login response."""
    return {
        "uid": user_record.uid,
        "email": user_record.email,
        "email_verified": user_record.email_verified,
        "display_name": user_record.display_name,
        "disabled": user_record.disabled,
        "created_at": user_record.user_metadata.creation_timestamp,
        "last_sign_in": user_record.user_metadata.last_sign_in_timestamp,
    }


def normalize_custom_token(uid: str) -> Dict[str, Any]:
    """Wrap a Firebase custom token in a standard response envelope."""
    return {"uid": uid, "auth_provider": "firebase"}
