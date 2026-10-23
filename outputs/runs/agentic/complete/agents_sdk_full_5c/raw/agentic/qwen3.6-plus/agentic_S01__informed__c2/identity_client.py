"""Local configuration and client helper utilities for Email/Password Account Lifecycle.

Provides Firebase Admin SDK initialization, credential loading from environment
variables, and shared client helpers used across the account lifecycle operations.
"""

import os
import json
import firebase_admin
from firebase_admin import credentials


def get_firebase_app(app_name: str = "__default__") -> firebase_admin.App:
    """Get or initialize the default Firebase Admin app instance.

    Loads the Firebase service account credentials from a JSON file path specified
    in the GOOGLE_APPLICATION_CREDENTIALS environment variable, or from inline
    environment variables (FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL,
    FIREBASE_PRIVATE_KEY).

    Args:
        app_name: The name for the Firebase app instance.

    Returns:
        Initialized firebase_admin.App instance.

    Raises:
        EnvironmentError: If credentials cannot be found or initialized.
    """
    # Return existing app if already initialized
    try:
        return firebase_admin.get_app(app_name)
    except ValueError:
        pass

    cred = _load_firebase_credentials()
    return firebase_admin.initialize_app(cred, name=app_name)


def _load_firebase_credentials() -> credentials.Certificate:
    """Load Firebase Admin credentials from environment.

    Priority:
      1. GOOGLE_APPLICATION_CREDENTIALS pointing to a service account JSON file.
      2. Individual environment variables: FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL,
         FIREBASE_PRIVATE_KEY.

    Returns:
        firebase_admin.credentials.Certificate instance.
    """
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path and os.path.isfile(cred_path):
        return credentials.Certificate(cred_path)

    # Fallback to individual env vars for service account JSON construction
    project_id = os.environ.get("FIREBASE_PROJECT_ID")
    client_email = os.environ.get("FIREBASE_CLIENT_EMAIL")
    private_key = os.environ.get("FIREBASE_PRIVATE_KEY")

    if project_id and client_email and private_key:
        # Normalize private key formatting
        key_value = private_key.replace("\\n", "\n")
        if not key_value.startswith("-----BEGIN"):
            key_value = f"-----BEGIN RSA PRIVATE KEY-----\n{key_value}\n-----END RSA PRIVATE KEY-----"

        service_account_info = {
            "type": "service_account",
            "project_id": project_id,
            "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", "unknown"),
            "private_key": key_value,
            "client_email": client_email,
            "client_id": os.environ.get("FIREBASE_CLIENT_ID", "0"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{client_email}",
        }

        return credentials.Certificate(service_account_info)

    raise EnvironmentError(
        "Firebase credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS to a "
        "service account JSON file, or provide FIREBASE_PROJECT_ID, "
        "FIREBASE_CLIENT_EMAIL, and FIREBASE_PRIVATE_KEY environment variables."
    )


def build_auth0_management_url(domain: str, path: str) -> str:
    """Build a full URL for the Auth0 Management API.

    Args:
        domain: Auth0 tenant domain (e.g., 'my-tenant.auth0.com').
        path: API path (e.g., '/api/v2/users').

    Returns:
        Full URL string.
    """
    return f"https://{domain.rstrip('/')}/{path.lstrip('/')}"
