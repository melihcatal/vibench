import requests
import jwt  # PyJWT library for decoding JWTs
from typing import Dict, Any
from identity_client import (
    GOOGLE_USERINFO_URL,
    GOOGLE_CLIENT_ID,
)  # GOOGLE_CLIENT_ID for ID token verification
from identity_models import UserProfileClaims, OAuthTokens


def fetch_and_normalize_profile_claims(oauth_tokens: OAuthTokens) -> UserProfileClaims:
    raw_claims: Dict[str, Any] = {}

    if oauth_tokens.id_token:
        # Google-specific: ID token contains user claims directly. Verify and decode it.
        # In a real application, you'd verify the ID token's signature, issuer, audience, and expiry.
        # For simplicity, we'll just decode it. A library like 'google-auth' would handle full verification.
        try:
            # Need to install pyjwt: pip install PyJWT
            # For full verification, you'd need Google's public certificates:
            # jwks_client = jwt.PyJWKClient("https://www.googleapis.com/oauth2/v3/certs")
            # signing_key = jwks_client.get_signing_key_from_jwt(oauth_tokens.id_token)
            # raw_claims = jwt.decode(oauth_tokens.id_token, signing_key.key, algorithms=["RS256"], audience=GOOGLE_CLIENT_ID)

            # For demonstration, decode without signature verification (DO NOT DO THIS IN PRODUCTION)
            raw_claims = jwt.decode(
                oauth_tokens.id_token, options={"verify_signature": False}
            )

        except Exception as e:
            print(f"Error decoding ID token: {e}")
            # Fallback to userinfo endpoint if ID token is invalid or absent
            raw_claims = _fetch_userinfo_from_endpoint(oauth_tokens.access_token)
    else:
        # If no ID token, use the userinfo endpoint with the access token
        raw_claims = _fetch_userinfo_from_endpoint(oauth_tokens.access_token)

    # Normalize claims from Google's response to our internal UserProfileClaims model
    normalized_claims = UserProfileClaims(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        email_verified=raw_claims.get("email_verified"),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=raw_claims.get("picture"),
        locale=raw_claims.get("locale"),
        hd=raw_claims.get("hd"),  # Google-specific hosted domain
        raw_claims=raw_claims,
    )
    return normalized_claims


def _fetch_userinfo_from_endpoint(access_token: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


if __name__ == "__main__":
    # Example Usage (requires a valid access token and optionally an ID token)
    # In a real scenario, these tokens would come from oauth_callback.py
    example_access_token = "YOUR_ACCESS_TOKEN"
    example_id_token = "YOUR_ID_TOKEN"  # Optional

    example_oauth_tokens = OAuthTokens(
        access_token=example_access_token,
        token_type="Bearer",
        expires_in=3600,
        id_token=example_id_token,
    )

    try:
        user_profile = fetch_and_normalize_profile_claims(example_oauth_tokens)
        print("Successfully fetched and normalized user profile claims:")
        print(f"Subject: {user_profile.sub}")
        print(f"Email: {user_profile.email}")
        print(f"Full Name: {user_profile.name}")
        print(f"Raw Claims: {user_profile.raw_claims}")
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching user info: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
