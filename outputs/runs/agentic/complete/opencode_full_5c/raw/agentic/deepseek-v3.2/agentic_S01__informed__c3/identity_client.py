import os
from auth0.authentication import GetToken
from auth0.management import Auth0


def get_auth0_client() -> Auth0:
    """Provide local configuration and client helper utilities for Auth0."""
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    if not domain or not client_id or not client_secret:
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET "
            "environment variables must be set"
        )

    get_token = GetToken(domain, client_id, client_secret=client_secret)
    token = get_token.client_credentials("https://{}/api/v2/".format(domain))
    mgmt_api_token = token["access_token"]

    return Auth0(domain, mgmt_api_token)


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"


def normalize_user_data(user_data: dict) -> dict:
    """Normalize user data for Auth0 API."""
    normalized = user_data.copy()

    if "name" in normalized:
        normalized["name"] = normalized["name"].strip()

    if "email" in normalized:
        normalized["email"] = normalized["email"].lower().strip()

    return normalized
