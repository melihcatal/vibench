import requests
from identity_client import IdentityClientConfig
from identity_models import UserProfileClaims


def fetch_google_profile_claims(access_token: str) -> UserProfileClaims:
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(
            IdentityClientConfig.GOOGLE_USERINFO_URL, headers=headers
        )
        response.raise_for_status()
        claims_data = response.json()

        return UserProfileClaims(
            sub=claims_data["sub"],
            name=claims_data.get("name"),
            given_name=claims_data.get("given_name"),
            family_name=claims_data.get("family_name"),
            email=claims_data.get("email"),
            email_verified=claims_data.get("email_verified"),
            picture=claims_data.get("picture"),
            locale=claims_data.get("locale"),
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch user profile claims from Google: {e}")


if __name__ == "__main__":
    # This is an example usage. In a real application, access_token would come from a completed OAuth flow.
    example_access_token = "YOUR_GOOGLE_ACCESS_TOKEN"
    if example_access_token != "YOUR_GOOGLE_ACCESS_TOKEN":
        try:
            profile = fetch_google_profile_claims(example_access_token)
            print(f"Successfully retrieved user profile claims: {profile}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(
            "Please replace 'YOUR_GOOGLE_ACCESS_TOKEN' with a valid access token to test."
        )
