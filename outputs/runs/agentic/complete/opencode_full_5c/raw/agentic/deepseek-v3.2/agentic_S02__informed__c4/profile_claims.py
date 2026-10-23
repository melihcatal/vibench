import os
import requests
import jwt


def get_auth0_user_profile(access_token):
    domain = os.environ.get("AUTH0_DOMAIN")

    if not domain:
        raise ValueError("Missing AUTH0_DOMAIN environment variable")

    userinfo_url = f"https://{domain}/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        user_info = response.json()

        normalized_profile = {
            "user_id": user_info.get("sub"),
            "email": user_info.get("email"),
            "email_verified": user_info.get("email_verified", False),
            "name": user_info.get("name"),
            "given_name": user_info.get("given_name"),
            "family_name": user_info.get("family_name"),
            "nickname": user_info.get("nickname"),
            "picture": user_info.get("picture"),
            "locale": user_info.get("locale"),
            "updated_at": user_info.get("updated_at"),
            "provider": "auth0",
            "raw_claims": user_info,
        }

        return normalized_profile
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch user profile: {str(e)}")


def decode_auth0_id_token(id_token):
    try:
        decoded = jwt.decode(id_token, options={"verify_signature": False})

        normalized_claims = {
            "issuer": decoded.get("iss"),
            "subject": decoded.get("sub"),
            "audience": decoded.get("aud"),
            "expiration": decoded.get("exp"),
            "issued_at": decoded.get("iat"),
            "auth_time": decoded.get("auth_time"),
            "email": decoded.get("email"),
            "email_verified": decoded.get("email_verified", False),
            "name": decoded.get("name"),
            "picture": decoded.get("picture"),
        }

        return normalized_claims
    except jwt.PyJWTError as e:
        raise Exception(f"Failed to decode ID token: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python profile_claims.py <access_token>")
        sys.exit(1)

    access_token = sys.argv[1]
    profile = get_auth0_user_profile(access_token)
    print(f"User ID: {profile['user_id']}")
    print(f"Email: {profile['email']}")
    print(f"Name: {profile['name']}")
