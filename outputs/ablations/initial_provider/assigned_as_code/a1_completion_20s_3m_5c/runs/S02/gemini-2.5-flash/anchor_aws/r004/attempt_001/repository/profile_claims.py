import os
import requests
import json

def fetch_and_normalize_profile_claims(access_token, config=None):
    config = config or {}
    domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"
    userinfo_url = domain + "/oauth2/userInfo"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        claims = response.json()
        
        # Normalize claims (example: simple mapping)
        normalized_claims = {
            "sub": claims.get("sub"),
            "email": claims.get("email"),
            "name": claims.get("username") # Cognito often uses 'username' instead of 'name'
        }
        return normalized_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info: {e}")
        return None
