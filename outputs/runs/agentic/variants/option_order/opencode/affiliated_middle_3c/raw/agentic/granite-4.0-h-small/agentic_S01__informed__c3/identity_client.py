import os
import json
import boto3

# Local helper to centralize configuration and client creation
REGION = os.getenv("AWS_REGION", "us-east-1")
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")

# Configure AWS clients once; reuse across modules
session = boto3.session.Session()
cognito_client = session.client(
    "cognito-idp",
    region_name=REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def get_user_pool_id():
    """Retrieve configured User Pool ID, raising if not set."""
    if not USER_POOL_ID:
        raise RuntimeError("COGNITO_USER_POOL_ID environment variable not defined")
    return USER_POOL_ID


def get_client_id():
    """Retrieve configured Client ID, raising if not set."""
    if not CLIENT_ID:
        raise RuntimeError("COGNITO_CLIENT_ID environment variable not defined")
    return CLIENT_ID


def call_cognito(method, **kwargs):
    """Thin wrapper that forwards calls to the cognito_client and returns the raw response."""
    return getattr(cognito_client, method)(**kwargs)


# Example helper: normalize signup payload
NORMALIZED_USER_ATTRIBUTES = {
    "email": "email",
    "first_name": "given_name",
    "last_name": "family_name",
}


def normalize_signup_payload(payload):
    """Convert UI-friendly keys to Cognito attribute names."""
    normalized = {}
    for key, value in payload.items():
        new_key = NORMALIZED_USER_ATTRIBUTES.get(key.lower(), key)
        normalized[new_key] = value
    # Force email attribute as required email type
    if "email" in normalized:
        normalized["email"] = {
            "Name": "email",
            "Value": normalized["email"],
            "Verified": False,
        }
    return normalized
