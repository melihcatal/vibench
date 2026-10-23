import os
import requests
from identity_models import NormalizedProfile

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")


def fetch_normalized_profile(access_token):
    userinfo_endpoint = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_endpoint, headers=headers)
    response.raise_for_status()
    claims = response.json()
    
    return NormalizedProfile(
        sub=claims.get("sub"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider="auth0"
    )