"""
Local configuration and client helper utilities for Email/Password Account Lifecycle
using Firebase Authentication as the concrete identity provider.
"""

import os
import json
import logging
from typing import Optional, Dict, Any

import firebase_admin
from firebase_admin import credentials, auth


logger = logging.getLogger(__name__)

# Firebase Auth provider identifiers
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "my-auth-project")
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "")
FIREBASE_AUTH_DOMAIN = os.environ.get("FIREBASE_AUTH_DOMAIN", f"{FIREBASE_PROJECT_ID}.firebaseapp.com")
FIREBASE_CREDENTIALS_PATH = os.environ.get("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY", "")

_firebase_app: Optional[firebase_admin.App] = None


def initialize_firebase_app(
    credentials_path: Optional[str] = None,
    project_id: Optional[str] = None,
) -> firebase_admin.App:
    """Initialize the Firebase Admin SDK application for Firebase Auth."""
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    cred_path = credentials_path or FIREBASE_CREDENTIALS_PATH
    proj_id = project_id or FIREBASE_PROJECT_ID

    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
    else:
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": proj_id,
            "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
            "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL", f"firebase-adminsdk@{proj_id}.iam.gserviceaccount.com"),
            "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", ""),
            "token_uri": "https://oauth2.googleapis.com/token",
        })

    _firebase_app = firebase_admin.initialize_app(cred, {
        "projectId": proj_id,
    })
    logger.info("Firebase Admin SDK initialized for project: %s", proj_id)
    return _firebase_app


def get_firebase_auth_client(app: Optional[firebase_admin.App] = None) -> auth.Client:
    """Return a Firebase Auth client instance."""
    target_app = app or _firebase_app
    if target_app is None:
        target_app = initialize_firebase_app()
    return auth.client(target_app)


def build_custom_token(
    uid: str,
    additional_claims: Optional[Dict[str, Any]] = None,
    app: Optional[firebase_admin.App] = None,
) -> str:
    """Build a custom Firebase Auth token for the given user ID."""
    target_app = app or _firebase_app or initialize_firebase_app()
    return auth.create_custom_token(uid, additional_claims, app=target_app)


def verify_id_token(
    id_token: str,
    app: Optional[firebase_admin.App] = None,
    check_revoked: bool = False,
) -> Dict[str, Any]:
    """Verify a Firebase ID token and return decoded claims."""
    target_app = app or _firebase_app or initialize_firebase_app()
    return auth.verify_id_token(id_token, app=target_app, check_revoked=check_revoked)


def get_firebase_rest_url(endpoint: str) -> str:
    """Construct a Firebase REST API URL."""
    base = "https://identitytoolkit.googleapis.com/v1"
    return f"{base}/{endpoint}?key={FIREBASE_WEB_API_KEY}"


def get_provider_config() -> Dict[str, str]:
    """Return the Firebase Auth provider configuration."""
    return {
        "provider": "firebase_auth",
        "project_id": FIREBASE_PROJECT_ID,
        "auth_domain": FIREBASE_AUTH_DOMAIN,
        "api_endpoint": "https://identitytoolkit.googleapis.com",
    }
