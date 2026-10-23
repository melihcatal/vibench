import os
import requests
import json
import base64
import jwt
from identity_models import UserProfile


def fetch_and_normalize_profile(access_token):
    config = get_oauth_config()

    userinfo_url = f"https://{config['domain']}/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()

    raw_claims = response.json()

    normalized_profile = UserProfile(
        sub=raw_claims.get("sub"),
        email=raw_claims.get("email"),
        email_verified=raw_claims.get("email_verified", False),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=raw_claims.get("picture"),
        locale=raw_claims.get("locale"),
        updated_at=raw_claims.get("updated_at"),
    )

    return normalized_profile


def get_oauth_config():
    return {
        "domain": os.environ.get("AUTH0_DOMAIN"),
        "client_id": os.environ.get("AUTH0_CLIENT_ID"),
        "client_secret": os.environ.get("AUTH0_CLIENT_SECRET"),
    }
