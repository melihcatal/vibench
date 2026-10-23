import os
import requests
import jwt

def fetch_and_normalize_profile_claims(access_token, config=None):
    config = config or {}
    region = config.get("region", os.environ.get("COGNITO_REGION"))
    userinfo_url = f"https://cognito-idp.{region}.amazonaws.com/oauth2/userInfo"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        claims = response.json()

        # Normalize claims (example normalization)
        normalized_claims = {
            "sub": claims.get("sub"),
            "email": claims.get("email"),
            "email_verified": claims.get("email_verified"),
            "name": claims.get("name", f"{claims.get('given_name', '')} {claims.get('family_name', '')}".strip()),
            "given_name": claims.get("given_name"),
            "family_name": claims.get("family_name"),
            "preferred_username": claims.get("preferred_username"),
            "locale": claims.get("locale"),
            "picture": claims.get("picture")
        }
        return {"profile_claims": normalized_claims}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error decoding or processing token: {e}"}
