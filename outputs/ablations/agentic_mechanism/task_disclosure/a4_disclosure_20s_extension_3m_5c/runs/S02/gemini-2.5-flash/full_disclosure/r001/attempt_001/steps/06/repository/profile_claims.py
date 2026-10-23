
import requests

def fetch_and_normalize_profile_claims(access_token: str) -> dict:
    """
    Fetches and normalizes federated user profile claims from Google.
    """
    google_userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(google_userinfo_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        user_info = response.json()

        # Normalize the claims
        normalized_claims = {
            "sub": user_info.get("sub"),
            "name": user_info.get("name"),
            "given_name": user_info.get("given_name"),
            "family_name": user_info.get("family_name"),
            "picture": user_info.get("picture"),
            "email": user_info.get("email"),
            "email_verified": user_info.get("email_verified"),
            "locale": user_info.get("locale"),
        }
        return normalized_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info from Google: {e}")
        return {}

