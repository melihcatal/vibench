from typing import Dict, Any
import os
import requests

# Google Identity Platform OIDC
GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"


def profile_claims(access_token: str) -> Dict[str, Any]:
    # Fetch user profile claims from Google
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(GOOGLE_USERINFO_ENDPOINT, headers=headers)
    response.raise_for_status()

    user_data = response.json()

    # Normalize claims
    return {
        "sub": user_data["sub"],
        "name": user_data.get("name"),
        "given_name": user_data.get("given_name"),
        "family_name": user_data.get("family_name"),
        "email": user_data.get("email"),
        "email_verified": user_data.get("email_verified", False),
        "picture": user_data.get("picture"),
        "locale": user_data.get("locale"),
    }
