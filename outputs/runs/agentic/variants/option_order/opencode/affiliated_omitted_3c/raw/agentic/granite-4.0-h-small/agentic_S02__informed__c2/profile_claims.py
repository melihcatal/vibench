import identity_client
import requests


def fetch_user_profile(access_token):
    # Example using Google Identity Platform OIDC to fetch normalized user profile claims
    # The token is an OIDC ID token that can be exchanged for profile info via Google UserInfo endpoint
    google_oauth2_client = identity_client.get_config("GOOGLE_OAUTH2_CLIENT")
    # Exchange token for userinfo payload
    userinfo_url = "https://oauth2.googleapis.com/tokeninfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(userinfo_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # Normalize claims: extract standard OIDC fields
    normalized = {
        "sub": data.get("sub"),
        "name": data.get("name"),
        "email": data.get("email"),
        "picture": data.get("picture"),
        "locale": data.get("locale"),
    }
    return normalized
