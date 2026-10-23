import os
import boto3
from botocore.exceptions import ClientError

# Core Cognito credentials - populated via environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")

# Create a reusable, thread-safe Cognito client
_cognito_client = None


def _get_cognito_client():
    global _cognito_client
    if _cognito_client is None:
        _cognito_client = boto3.client(
            "cognito-idp",
            region_name=REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    return _cognito_client


# ---------------------------------------------------------------------
# User Registration
# ---------------------------------------------------------------------


def register_user(email, password, attributes=None):
    """Creates a new email/password user account in Cognito.

    Args:
        email (str): User email.
        password (str): Plain-text password.
        attributes (list, optional): List of dicts like [{\"Name\": \"custom:role\", \"Value\": \"admin\"}].

    Returns:
        dict: Cognito response.
    """
    client = _get_cognito_client()
    try:
        return client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=attributes or [],
        )
    except ClientError as exc:
        raise RuntimeError(f"Registration failed for {email!r}: {exc}")


# ---------------------------------------------------------------------
# Authentication (login)
# ---------------------------------------------------------------------


def authenticate(email, password):
    """Exchange username/password for tokens using Admin API.

    Args:
        email (str): Registered email.
        password (str): Plain-text password.

    Returns:
        dict: Contains IdToken, AccessToken, RefreshToken.
    """
    client = _get_cognito_client()
    try:
        return client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
    except ClientError as exc:
        raise RuntimeError(f"Login failed for {email!r}: {exc}")


# ---------------------------------------------------------------------
# Token Refresh (using Identity Pool)
# ---------------------------------------------------------------------
IDENTITY_POOL_ID = os.getenv("COGNITO_IDENTITY_POOL_ID")


def refresh_tokens(id_token):
    """Validate an ID token via an Identity Pool and return fresh AWS credentials.

    Args:
        id_token (str): Valid ID token from Cognito.

    Returns:
        dict: AWS credentials with AccessKeyId, SecretKey, SessionToken.
    """
    ident_client = boto3.client(
        "cognito-identity",
        region_name=REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    try:
        # First get an IdentityId (no token required)
        identity_response = ident_client.get_id(IdentityPoolId=IDENTITY_POOL_ID)
        identity_id = identity_response["IdentityId"]

        # Exchange the Cognito token for fresh temporary AWS credentials
        cred_response = ident_client.get_credentials_for_identity(
            IdentityId=identity_id,
            Logins={
                "cognito-idp.<region>.amazonaws.com/<user-pool-id>": id_token,
            },
        )
        return {
            "AccessKeyId": cred_response["AccessKeyId"],
            "SecretKey": cred_response["SecretKey"],
            "SessionToken": cred_response["SessionToken"],
        }
    except ClientError as exc:
        raise RuntimeError(f"Token refresh failed: {exc}")


# ---------------------------------------------------------------------
# Password Reset
# ---------------------------------------------------------------------


def forgot_password(email):
    """Initiates a password reset that sends a verification code to the user.

    Args:
        email (str): Registered email.

    Returns:
        dict: Cognito response.
    """
    client = _get_cognito_client()
    try:
        return client.forgot_password(
            ClientId=CLIENT_ID,
            Username=email,
        )
    except ClientError as exc:
        raise RuntimeError(f"Forgot password request failed for {email!r}: {exc}")


def confirm_password_reset(email, code, new_password):
    """Completes the password reset using the verification code.

    Args:
        email (str): Registered email.
        code (str): Verification code sent via email or SMS.
        new_password (str): New password.

    Returns:
        dict: Cognito response.
    """
    client = _get_cognito_client()
    try:
        return client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=code,
            Password=new_password,
        )
    except ClientError as exc:
        raise RuntimeError(f"Confirm password reset failed for {email!r}: {exc}")


# ---------------------------------------------------------------------
# Utility Helpers
# ---------------------------------------------------------------------


def _normalize_attribute_list(attrs):
    """Converts a list of dicts with \"Name\" and \"Value\" to the format Cognito expects."""
    if not attrs:
        return []
    normalized = []
    for a in attrs:
        if isinstance(a, dict) and set(a.keys()) == {"Name", "Value"}:
            normalized.append(a)
        else:
            # Assume simple name/value pair dict-like object
            normalized.append({"Name": a["name"], "Value": a["value"]})
    return normalized
