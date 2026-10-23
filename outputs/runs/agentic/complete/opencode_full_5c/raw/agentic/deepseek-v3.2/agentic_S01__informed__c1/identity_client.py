import os
import boto3
from botocore.config import Config


def get_cognito_client():
    """Get Amazon Cognito client with configuration."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    return boto3.client("cognito-idp", config=config)


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"

    return True, "Password is valid"


def get_user_pool_id() -> str:
    """Get Cognito User Pool ID from environment."""
    return os.environ.get("COGNITO_USER_POOL_ID", "")


def get_client_id() -> str:
    """Get Cognito Client ID from environment."""
    return os.environ.get("COGNITO_CLIENT_ID", "")
