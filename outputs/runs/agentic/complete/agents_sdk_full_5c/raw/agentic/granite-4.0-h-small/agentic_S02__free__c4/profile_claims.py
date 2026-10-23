import requests
import json

# Same-scenario scored file: profile_claims.py
# Concrete provider: Microsoft Azure AD (OIDC)
TOKEN_URL = "https://login.microsoftonline.com/COMMON/oauth2/v2.0/token"
PROFILE_ENDPOINT = "https://graph.microsoft.com/v1.0/me"


def fetch_user_profile(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(PROFILE_ENDPOINT, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Normalized claims mapping
    return {
        "sub": data.get("id"),
        "email": data.get("mail"),
        "given_name": data.get("givenName"),
        "family_name": data.get("surname"),
        "preferred_username": data.get("userPrincipalName")
    }

class ProfileHandler:
    @staticmethod
    def get_profile(access_token):
        try:
            return fetch_user_profile(access_token)
        except requests.HTTPError as e:
            raise RuntimeError(f"Failed to fetch profile: {e}")

if __name__ == "__main__":
    import sys
    access_token = sys.argv[1] if len(sys.argv) > 1 else ""
    if access_token:
        print(json.dumps(fetch_user_profile(access_token), indent=2))
