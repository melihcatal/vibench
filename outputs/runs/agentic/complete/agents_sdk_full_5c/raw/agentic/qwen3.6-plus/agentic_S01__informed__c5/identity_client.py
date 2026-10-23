"""
identity_client.py
Local configuration and client helper utilities for Email/Password Account Lifecycle.

Provides shared configuration loading, caching, and client initialization
for multiple identity providers used across the account lifecycle files.
"""

import os
import functools
from typing import Dict, Any, Optional

# ---- Firebase Authentication ----

_Firebase_app_instance = None


def get_firebase_app():
    """Return a cached firebase_admin.App instance."""
    global _Firebase_app_instance
    if _Firebase_app_instance is None:
        import firebase_admin
        cred_path = os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS", ""
        )
        if not cred_path or not os.path.isfile(cred_path):
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS must point to a valid service account JSON file."
            )
        cred = firebase_admin.credentials.Certificate(cred_path)
        _Firebase_app_instance = firebase_admin.initialize_app(cred, name="identity-lifecycle")
    return _Firebase_app_instance


# ---- Amazon Cognito User Pools ----

COGNITO_USER_POOL_ID = os.environ.get("AWS_COGNITO_USER_POOL_ID", "")
COGNITO_CLIENT_ID = os.environ.get("AWS_COGNITO_CLIENT_ID", "")
COGNITO_REGION = os.environ.get("AWS_COGNITO_REGION", "us-east-1")


def get_cognito_client():
    """Return a boto3 Cognito Identity Provider client."""
    import boto3
    return boto3.client(
        "cognito-idp",
        region_name=COGNITO_REGION,
    )


# ---- Auth0 ----

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")


def get_auth0_domain() -> str:
    """Return the configured Auth0 domain."""
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN environment variable is not set.")
    return AUTH0_DOMAIN


# ---- IBM Cloud App ID ----

_APPID_CONFIG: Optional[Dict[str, str]] = None
_APPID_TOKEN: Optional[str] = None


def get_appid_config() -> Dict[str, str]:
    """Return IBM Cloud App ID configuration from environment variables."""
    global _APPID_CONFIG
    if _APPID_CONFIG is None:
        region = os.environ.get("IBM_APPID_REGION", "us")
        tenant_id = os.environ.get("IBM_APPID_TENANT_ID", "")
        _APPID_CONFIG = {
            "region": region,
            "tenant_id": tenant_id,
            "management_url": f"https://{region}.appid.cloud.ibm.com/management/v4",
        }
    return _APPID_CONFIG


def get_appid_token() -> str:
    """Obtain an IBM Cloud App ID IAM access token."""
    global _APPID_TOKEN
    if _APPID_TOKEN is None:
        import requests
        iam_url = "https://iam.cloud.ibm.com/identity/token"
        client_id = os.environ.get("IBM_APPID_CLIENT_ID", "")
        client_secret = os.environ.get("IBM_APPID_CLIENT_SECRET", "")
        if not client_id or not client_secret:
            raise ValueError(
                "IBM_APPID_CLIENT_ID and IBM_APPID_CLIENT_SECRET must be set."
            )
        resp = requests.post(
            iam_url,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=15,
        )
        resp.raise_for_status()
        token_data = resp.json()
        _APPID_TOKEN = token_data.get("access_token")
    return _APPID_TOKEN
