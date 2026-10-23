"""
Local configuration and client helper utilities for Email/Password Account Lifecycle.

Provides a thin wrapper around firebase-admin for Auth operations,
configuration loading, and Firebase REST API helpers for login, refresh,
and password reset flows that use the Firebase Identity Toolkit REST endpoints.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin._auth_client import Auth as FirebaseAuthClient


FIREBASE_AUTH_REST_BASE = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_DEFAULT_API_KEY_ENV = "FIREBASE_WEB_API_KEY"


def _get_firebase_api_key() -> str:
    api_key = os.environ.get(FIREBASE_DEFAULT_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"Environment variable {FIREBASE_DEFAULT_API_KEY_ENV} is not set. "
            "Firebase Web API key is required for REST auth flows."
        )
    return api_key


def _get_firebase_project_id() -> str:
    project_id = os.environ.get("FIREBASE_PROJECT_ID")
    if not project_id:
        raise RuntimeError(
            "FIREBASE_PROJECT_ID environment variable is not set."
        )
    return project_id


def initialize_firebase_app() -> firebase_admin.App:
    """
    Initialize the default Firebase app if not already initialized.
    Uses GOOGLE_APPLICATION_CREDENTIALS or explicit service-account path.
    """
    if firebase_admin._apps:
        return firebase_admin.get_app()

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path and os.path.isfile(cred_path):
        cred = credentials.Certificate(cred_path)
    else:
        cred = credentials.ApplicationDefault()

    project_id = _get_firebase_project_id()
    return firebase_admin.initialize_app(cred, {"projectId": project_id})


def get_firebase_auth_client() -> FirebaseAuthClient:
    """Return the Firebase Admin Auth client for server-side operations."""
    app = initialize_firebase_app()
    return auth._get_client(app)


def build_firebase_rest_url(method: str) -> str:
    """Build a full Firebase Identity Toolkit REST endpoint URL."""
    api_key = _get_firebase_api_key()
    return f"{FIREBASE_AUTH_REST_BASE}/accounts:{method}?key={api_key}"


def build_firebase_oob_rest_url(method: str) -> str:
    """Build a Firebase Identity Toolkit OOB (out-of-band) REST endpoint URL."""
    api_key = _get_firebase_api_key()
    return f"{FIREBASE_AUTH_REST_BASE}/accounts:{method}?key={api_key}"


def create_firebase_user(
    email: str,
    password: str,
    display_name: Optional[str] = None,
    custom_claims: Optional[Dict[str, Any]] = None,
) -> auth.UserRecord:
    """
    Create a new user via Firebase Admin SDK.
    This uses the firebase-admin SDK's auth.create_user which connects
    to the Google Identity Toolkit API for the configured Firebase project.
    """
    user_params: Dict[str, Any] = {
        "email": email,
        "password": password,
    }
    if display_name:
        user_params["display_name"] = display_name

    user_record = auth.create_user(**user_params)

    if custom_claims:
        auth.set_custom_user_claims(user_record.uid, custom_claims)

    return user_record
