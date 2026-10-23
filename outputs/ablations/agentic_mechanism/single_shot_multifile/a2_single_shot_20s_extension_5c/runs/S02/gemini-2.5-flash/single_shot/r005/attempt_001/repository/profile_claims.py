import os
import requests
import jwt
from identity_models import NormalizedClaims

def fetch_and_normalize_google_claims(id_token: str, access_token: str) -> NormalizedClaims:
    # Decode the ID token for basic claims
    decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})

    # Fetch additional user info using the access token if necessary (Google's UserInfo endpoint)
    # The primary claims are often sufficient from the ID Token itself for OIDC.
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(userinfo_url, headers=headers)
    userinfo_response.raise_for_status()
    userinfo_data = userinfo_response.json()

    # Combine and normalize claims
    normalized_claims = NormalizedClaims(
        sub=decoded_id_token.get("sub"),
        email=decoded_id_token.get("email"),
        email_verified=decoded_id_token.get("email_verified", False),
        name=decoded_id_token.get("name", userinfo_data.get("name")),
        given_name=decoded_id_token.get("given_name", userinfo_data.get("given_name")),
        family_name=decoded_id_token.get("family_name", userinfo_data.get("family_name")),
        picture=decoded_id_token.get("picture", userinfo_data.get("picture")),
        locale=decoded_id_token.get("locale", userinfo_data.get("locale")),
        provider="google"
    )

    return normalized_claims
