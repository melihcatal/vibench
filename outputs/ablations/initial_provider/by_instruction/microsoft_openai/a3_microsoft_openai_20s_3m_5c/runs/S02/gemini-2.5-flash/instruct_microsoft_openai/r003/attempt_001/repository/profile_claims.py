import requests
import jwt
from typing import Dict, Any, Optional

from identity_client import IdentityClientConfig
from identity_models import UserProfile, TokenResponse

def fetch_and_normalize_profile_claims(token_response: TokenResponse) -> Optional[UserProfile]:
    # First, try to get claims from the ID Token if available
    if token_response.id_token:
        try:
            # The ID Token is a JWT, decode it to get claims
            # In a real application, you would also verify the signature and claims (e.g., audience, issuer, expiry)
            id_token_claims = jwt.decode(token_response.id_token, options={"verify_signature": False})
            print("Decoded claims from ID Token.")
            return _normalize_claims(id_token_claims)
        except Exception as e:
            print(f"Error decoding ID Token: {e}")

    # If no ID token or decoding failed, try fetching from Microsoft Graph API using the access token
    if token_response.access_token:
        headers = {
            "Authorization": f"Bearer {token_response.access_token}"
        }
        try:
            print(f"Fetching user profile from Microsoft Graph API: {IdentityClientConfig.AZURE_AD_GRAPH_ENDPOINT}")
            response = requests.get(IdentityClientConfig.AZURE_AD_GRAPH_ENDPOINT, headers=headers)
            response.raise_for_status()
            graph_profile_data = response.json()
            print("Successfully fetched profile from Microsoft Graph.")
            return _normalize_claims(graph_profile_data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile from Microsoft Graph: {e}")
            if response:
                print(f"Response content: {response.text}")

    print("Could not fetch or normalize profile claims.")
    return None

def _normalize_claims(claims: Dict[str, Any]) -> UserProfile:
    # Normalize claims from different sources (ID Token, Graph API) into a common UserProfile model
    normalized_profile = UserProfile(
        sub=claims.get("sub", claims.get("oid")), # 'sub' from ID Token, 'oid' from Graph for user ID
        name=claims.get("name", claims.get("displayName")),
        email=claims.get("email", claims.get("userPrincipalName")),
        given_name=claims.get("given_name", claims.get("givenName")),
        family_name=claims.get("family_name", claims.get("surname")),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        raw_claims=claims
    )
    print("Normalized user profile claims.")
    return normalized_profile

if __name__ == "__main__":
    # Example usage: Simulate with a dummy token response
    dummy_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJlbWFpbCI6ImpvaG5kb2VAZXhhbXBsZS5jb20ifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    dummy_id_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzb21lX3VzZXJfaWQiLCJuYW1lIjoiRXhhbXBsZSBVc2VyIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaXNzIjoiaHR0cHM6Ly9leGFtcGxlLWFkLmNvbS90ZW5hbnRfaWQvdjIuMCIsImF1ZCI6ImNsaWVudF9pZCJ9.some_signature_part"

    dummy_token_response = TokenResponse(
        access_token=dummy_access_token,
        token_type="Bearer",
        expires_in=3600,
        scope="openid profile email User.Read",
        id_token=dummy_id_token
    )

    # In a real application, you would pass a valid TokenResponse object obtained from oauth_callback.py
    user_profile = fetch_and_normalize_profile_claims(dummy_token_response)

    if user_profile:
        print("\n--- Normalized User Profile ---")
        print(f"Subject (sub/oid): {user_profile.sub}")
        print(f"Name: {user_profile.name}")
        print(f"Email: {user_profile.email}")
        print(f"Raw Claims: {user_profile.raw_claims}")
