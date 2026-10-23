import requests
from identity_client import get_auth0_config, build_auth0_userinfo_url
from identity_models import normalize_claims


def fetch_and_normalize_profile_claims(access_token: str) -> dict:
    config = get_auth0_config()
    if not config["DOMAIN"]:
        raise ValueError("Auth0 DOMAIN environment variable is not set.")

    userinfo_url = build_auth0_userinfo_url(config)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()

    raw_claims = response.json()
    normalized_claims = normalize_claims(raw_claims)
    return normalized_claims


if __name__ == "__main__":
    # Example usage: This would typically be called after successfully getting an access token.
    # Set dummy environment variables for demonstration
    import os

    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"

    sample_access_token = "dummy_access_token"
    try:
        print("Simulating fetching and normalizing profile claims...")
        profile = fetch_and_normalize_profile_claims(sample_access_token)
        print("User Profile Claims:")
        print(profile)
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
