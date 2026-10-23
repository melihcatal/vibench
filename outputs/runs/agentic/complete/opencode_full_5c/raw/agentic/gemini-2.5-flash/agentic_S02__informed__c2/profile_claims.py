import os
import requests
from identity_models import UserProfileClaims

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")


def fetch_user_profile_claims(access_token: str) -> UserProfileClaims:
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims_data = response.json()
    return UserProfileClaims(
        sub=claims_data.get("sub"),
        name=claims_data.get("name"),
        email=claims_data.get("email"),
        email_verified=claims_data.get("email_verified"),
        picture=claims_data.get("picture"),
        updated_at=claims_data.get("updated_at"),
        # Add other claims as needed
    )


if __name__ == "__main__":
    # Example usage:
    # Set environment variable AUTH0_DOMAIN
    # from oauth_callback import handle_oauth_callback
    # auth_code = "YOUR_AUTHORIZATION_CODE"
    # tokens = handle_oauth_callback(auth_code)
    # access_token = tokens["access_token"]
    # profile = fetch_user_profile_claims(access_token)
    # print(profile.to_dict())
    pass
