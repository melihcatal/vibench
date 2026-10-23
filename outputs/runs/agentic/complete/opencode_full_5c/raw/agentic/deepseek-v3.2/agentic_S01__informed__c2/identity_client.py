import os
from auth0.authentication import GetToken
from auth0.management import Auth0


def get_auth0_client() -> Auth0:
    """Initialize and return an Auth0 management API client."""
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")

    if not all([domain, client_id, client_secret]):
        raise ValueError(
            "Missing Auth0 environment variables: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET"
        )

    get_token = GetToken(domain, client_id, client_secret=client_secret)
    token = get_token.client_credentials("https://{}/api/v2/".format(domain))
    mgmt_api_token = token["access_token"]

    return Auth0(domain, mgmt_api_token)


def validate_email(email: str) -> bool:
    """Basic email validation."""
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


def normalize_user_data(email: str, name: str = None) -> dict:
    """Normalize user data for consistent API calls."""
    normalized = {
        "email": email.lower().strip(),
        "email_verified": False,
        "connection": "Username-Password-Authentication",
    }

    if name:
        normalized["name"] = name.strip()
        parts = name.strip().split()
        if len(parts) >= 2:
            normalized["given_name"] = parts[0]
            normalized["family_name"] = " ".join(parts[1:])
        else:
            normalized["given_name"] = name.strip()

    return normalized
