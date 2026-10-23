import os
import json
import jwt # PyJWT
import requests

# Using Auth0 for federated user profile claims
# Provider: Auth0 Authentication API
# Identifiable signal: AUTH0_DOMAIN, jwt decoding (for ID token), requests to Auth0 /userinfo endpoint

def fetch_and_normalize_profile_claims(id_token: str = None, access_token: str = None) -> dict:
    """
    Fetches and normalizes federated user profile claims either from an ID token
    or by calling the Auth0 /userinfo endpoint with an access token.

    Args:
        id_token: The ID token received from the OIDC provider.
        access_token: The access token received from the OIDC provider.

    Returns:
        A dictionary containing normalized user profile claims.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

    if not AUTH0_DOMAIN:
        raise ValueError("Missing Auth0_DOMAIN environment variable.")

    profile_claims = {}

    if id_token:
        try:
            # In a real application, you would also verify the signature and expiry
            # This requires fetching Auth0's public keys (JWKS endpoint)
            # For simplicity, we are just decoding without verification here.
            # A library like `python-jose` or `Auth0-Python` SDK handles this securely.
            decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})

            profile_claims["user_id"] = decoded_id_token.get("sub")
            profile_claims["name"] = decoded_id_token.get("name")
            profile_claims["email"] = decoded_id_token.get("email")
            profile_claims["picture"] = decoded_id_token.get("picture")
            profile_claims["preferred_username"] = decoded_id_token.get("nickname")
            profile_claims["given_name"] = decoded_id_token.get("given_name")
            profile_claims["family_name"] = decoded_id_token.get("family_name")

        except jwt.PyJWTError as e:
            print(f"Error decoding ID token: {e}")
            # Fallback to userinfo if ID token is invalid or cannot be decoded securely
            if not access_token:
                raise

    if access_token and not profile_claims.get("user_id"): # Only fetch if ID token didn't provide enough info
        userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            response = requests.get(userinfo_url, headers=headers)
            response.raise_for_status()
            userinfo = response.json()

            # Update claims with info from userinfo endpoint
            profile_claims["user_id"] = userinfo.get("sub")
            profile_claims["name"] = userinfo.get("name", profile_claims.get("name"))
            profile_claims["email"] = userinfo.get("email", profile_claims.get("email"))
            profile_claims["picture"] = userinfo.get("picture", profile_claims.get("picture"))
            profile_claims["preferred_username"] = userinfo.get("nickname", profile_claims.get("preferred_username"))
            profile_claims["given_name"] = userinfo.get("given_name", profile_claims.get("given_name"))
            profile_claims["family_name"] = userinfo.get("family_name", profile_claims.get("family_name"))

        except requests.exceptions.RequestException as e:
            print(f"Error fetching userinfo: {e}")
            if not profile_claims: # If no claims from ID token either
                raise

    # Normalize to a common structure
    normalized_claims = {
        "id": profile_claims.get("user_id"),
        "display_name": profile_claims.get("name", profile_claims.get("preferred_username", profile_claims.get("email"))),
        "email": profile_claims.get("email"),
        "avatar_url": profile_claims.get("picture"),
        "first_name": profile_claims.get("given_name"),
        "last_name": profile_claims.get("family_name"),
        "raw_claims": profile_claims # Store all fetched claims for auditing/debugging
    }

    return normalized_claims

if __name__ == '__main__':
    # Example usage (requires an ID token or access token)
    # In a real app, these would come from the session after oauth_callback
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"

    # Mock data for demonstration
    # IMPORTANT: In a real app, never hardcode tokens or use unverified tokens directly.
    # Use a proper JWT library with key verification for production.
    mock_id_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwiYmFzZW9fdXNlcl9pZCI6IjY1NDMyMSIsIm5hbWUiOiJKb2huIERvZSIsImVtYWlsIjoiam9obmRvZUBleGFtcGxlLmNvbSIsIm5pY2tuYW1lIjoiSm9lIiwiZ2l2ZW5fZm5hbWUiOiJKb2huIiwiZmFtaWx5X25hbWUiOiJEb2UiLCJwaWN0dXJlIjoiaHR0cHM6Ly9leGFtcGxlLmNvbS9hcGkvZmFrZWF2YXRhci5wbmciLCJpYXQiOjE1MTYyMzkwMjJ9."
        "_signature_is_not_verified_in_this_example"
    )
    mock_access_token = "some_mock_access_token_from_auth0"

    print("\n--- Claims from ID Token (mocked) ---")
    try:
        claims_from_id_token = fetch_and_normalize_profile_claims(id_token=mock_id_token)
        print(json.dumps(claims_from_id_token, indent=2))
    except Exception as e:
        print(f"Could not process ID token: {e}")

    print("\n--- Claims from Access Token (mocked) ---")
    # This would typically involve a real network call, so we'll simulate success
    # For a real run, ensure AUTH0_DOMAIN is correct and an active access_token is used
    try:
        # For demonstration, let's assume the userinfo endpoint returns this:
        # 'requests.get(...).json()' would return something like:
        # {"sub": "auth0|12345", "nickname": "testuser", "name": "Test User", "picture": "https://example.com/avatar.png", "email": "test@example.com"}
        print("Simulating fetching userinfo with access token...")
        # To make this runnable without a live token, we'll mock the requests call
        class MockResponse:
            def __init__(self, json_data, status_code=200):
                self._json_data = json_data
                self.status_code = status_code

            def json(self):
                return self._json_data

            def raise_for_status(self):
                if self.status_code >= 400:
                    raise requests.exceptions.RequestException(f"HTTP {self.status_code}")

        original_requests_get = requests.get
        requests.get = lambda url, headers: MockResponse({
            "sub": "auth0|mock_user_id_from_access_token",
            "nickname": "AccessTokenUser",
            "name": "Access Token User",
            "email": "access.token.user@example.com",
            "picture": "https://example.com/access_token_avatar.png",
            "given_name": "Access",
            "family_name": "TokenUser"
        }) if "userinfo" in url else original_requests_get(url, headers)

        claims_from_access_token = fetch_and_normalize_profile_claims(access_token=mock_access_token)
        print(json.dumps(claims_from_access_token, indent=2))

        requests.get = original_requests_get # Restore original requests.get

    except Exception as e:
        print(f"Could not process Access token for userinfo: {e}")
