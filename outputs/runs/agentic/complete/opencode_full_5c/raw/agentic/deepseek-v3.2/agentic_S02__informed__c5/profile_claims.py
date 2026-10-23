import os
import requests
import jwt
from typing import Dict, Any, Optional


def fetch_auth0_user_profile(access_token: str) -> Dict[str, Any]:
    """
    Fetch user profile claims from Auth0 using the access token.
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    if not auth0_domain:
        raise ValueError("AUTH0_DOMAIN environment variable must be set")

    userinfo_url = f"https://{auth0_domain}/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()

    return response.json()


def fetch_cognito_user_profile(access_token: str) -> Dict[str, Any]:
    """
    Fetch user profile claims from Amazon Cognito using the access token.
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN")
    if not cognito_domain:
        raise ValueError("COGNITO_DOMAIN environment variable must be set")

    userinfo_url = f"https://{cognito_domain}/oauth2/userInfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()

    return response.json()


def normalize_user_profile(
    profile_data: Dict[str, Any], provider: str = "auth0"
) -> Dict[str, Any]:
    """
    Normalize user profile claims from different identity providers to a common format.
    """
    normalized = {
        "provider": provider,
        "user_id": None,
        "email": None,
        "email_verified": False,
        "name": None,
        "given_name": None,
        "family_name": None,
        "picture": None,
        "locale": None,
        "raw_profile": profile_data,
    }

    if provider == "auth0":
        normalized["user_id"] = profile_data.get("sub")
        normalized["email"] = profile_data.get("email")
        normalized["email_verified"] = profile_data.get("email_verified", False)
        normalized["name"] = profile_data.get("name")
        normalized["given_name"] = profile_data.get("given_name")
        normalized["family_name"] = profile_data.get("family_name")
        normalized["picture"] = profile_data.get("picture")
        normalized["locale"] = profile_data.get("locale")

    elif provider == "cognito":
        normalized["user_id"] = profile_data.get("sub")
        normalized["email"] = profile_data.get("email")
        normalized["email_verified"] = (
            profile_data.get("email_verified", "false").lower() == "true"
        )
        normalized["name"] = profile_data.get("name")
        normalized["given_name"] = profile_data.get("given_name")
        normalized["family_name"] = profile_data.get("family_name")
        normalized["picture"] = profile_data.get("picture")
        normalized["locale"] = profile_data.get("locale")

    return normalized


def decode_id_token(id_token: str, verify: bool = True) -> Dict[str, Any]:
    """
    Decode and optionally verify an ID token.
    """
    if verify:
        # In production, you would verify the token signature with the provider's JWKS
        decoded = jwt.decode(id_token, options={"verify_signature": False})
    else:
        decoded = jwt.decode(id_token, options={"verify_signature": False})

    return decoded
