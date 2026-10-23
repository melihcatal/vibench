import os
import json
import jwt
import requests
from auth0.authentication import Users


def get_user_profile(access_token):
    domain = os.environ.get("AUTH0_DOMAIN")

    if not domain:
        raise ValueError("AUTH0_DOMAIN environment variable is required")

    userinfo_url = f"https://{domain}/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch user profile: {response.text}")

    user_info = response.json()

    normalized_profile = normalize_profile_claims(user_info)

    return normalized_profile


def normalize_profile_claims(raw_claims):
    normalized = {
        "user_id": raw_claims.get("sub", ""),
        "email": raw_claims.get("email", ""),
        "email_verified": raw_claims.get("email_verified", False),
        "name": raw_claims.get("name", ""),
        "given_name": raw_claims.get("given_name", ""),
        "family_name": raw_claims.get("family_name", ""),
        "nickname": raw_claims.get("nickname", ""),
        "picture": raw_claims.get("picture", ""),
        "locale": raw_claims.get("locale", "en"),
        "updated_at": raw_claims.get("updated_at", ""),
    }

    if "https://" in normalized["user_id"]:
        normalized["provider"] = "auth0"
    else:
        normalized["provider"] = "unknown"

    return normalized


def fetch_and_normalize_profile(access_token):
    try:
        profile = get_user_profile(access_token)
        return profile
    except Exception as e:
        print(f"Error fetching profile claims: {e}")
        raise
