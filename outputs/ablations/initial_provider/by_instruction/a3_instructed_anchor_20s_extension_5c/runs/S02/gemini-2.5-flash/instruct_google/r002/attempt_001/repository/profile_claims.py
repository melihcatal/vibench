import requests

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def fetch_google_profile_claims(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    response.raise_for_status()
    claims = response.json()
    return normalize_google_claims(claims)

def normalize_google_claims(claims: dict):
    # Basic normalization for Google claims
    normalized_claims = {
        "sub": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
    }
    return normalized_claims
