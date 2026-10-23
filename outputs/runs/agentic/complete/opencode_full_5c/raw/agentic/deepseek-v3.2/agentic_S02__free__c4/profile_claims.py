import os
import requests
import jwt
from typing import Dict, Any


def fetch_user_profile(access_token: str, provider: str = "google") -> Dict[str, Any]:
    if provider == "google":
        userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(userinfo_endpoint, headers=headers)

        if response.status_code == 200:
            profile_data = response.json()

            normalized_profile = {
                "id": profile_data.get("sub"),
                "email": profile_data.get("email"),
                "email_verified": profile_data.get("email_verified", False),
                "name": profile_data.get("name"),
                "given_name": profile_data.get("given_name"),
                "family_name": profile_data.get("family_name"),
                "picture": profile_data.get("picture"),
                "locale": profile_data.get("locale"),
                "provider": "google",
            }

            return normalized_profile
        else:
            raise Exception(f"Failed to fetch Google profile: {response.text}")

    elif provider == "github":
        user_endpoint = "https://api.github.com/user"
        email_endpoint = "https://api.github.com/user/emails"

        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        user_response = requests.get(user_endpoint, headers=headers)

        if user_response.status_code == 200:
            user_data = user_response.json()

            email_response = requests.get(email_endpoint, headers=headers)
            email_data = (
                email_response.json() if email_response.status_code == 200 else []
            )

            primary_email = None
            for email in email_data:
                if email.get("primary"):
                    primary_email = email.get("email")
                    break

            if not primary_email and email_data:
                primary_email = email_data[0].get("email")

            normalized_profile = {
                "id": str(user_data.get("id")),
                "login": user_data.get("login"),
                "email": primary_email,
                "email_verified": True,
                "name": user_data.get("name"),
                "avatar_url": user_data.get("avatar_url"),
                "company": user_data.get("company"),
                "blog": user_data.get("blog"),
                "location": user_data.get("location"),
                "bio": user_data.get("bio"),
                "provider": "github",
            }

            return normalized_profile
        else:
            raise Exception(f"Failed to fetch GitHub profile: {user_response.text}")

    elif provider == "auth0":
        domain = os.environ.get("AUTH0_DOMAIN")
        userinfo_endpoint = f"https://{domain}/userinfo"

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(userinfo_endpoint, headers=headers)

        if response.status_code == 200:
            profile_data = response.json()

            normalized_profile = {
                "id": profile_data.get("sub"),
                "email": profile_data.get("email"),
                "email_verified": profile_data.get("email_verified", False),
                "name": profile_data.get("name"),
                "nickname": profile_data.get("nickname"),
                "picture": profile_data.get("picture"),
                "provider": "auth0",
            }

            return normalized_profile
        else:
            raise Exception(f"Failed to fetch Auth0 profile: {response.text}")

    else:
        raise ValueError(f"Unsupported provider: {provider}")
