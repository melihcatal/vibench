import requests
from identity_client import get_cognito_config
from identity_models import UserProfile
import jwt

def fetch_user_profile(access_token: str, id_token: str) -> UserProfile:
    config = get_cognito_config()
    userinfo_endpoint = config.userinfo_endpoint

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(userinfo_endpoint, headers=headers)
        response.raise_for_status()
        userinfo = response.json()

        # Decode ID token to get additional claims
        decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})

        profile = UserProfile(
            sub=userinfo.get("sub", decoded_id_token.get("sub")),
            email=userinfo.get("email", decoded_id_token.get("email")),
            email_verified=userinfo.get("email_verified", decoded_id_token.get("email_verified")),
            preferred_username=userinfo.get("preferred_username", decoded_id_token.get("preferred_username")),
            given_name=userinfo.get("given_name", decoded_id_token.get("given_name")),
            family_name=userinfo.get("family_name", decoded_id_token.get("family_name")),
            name=userinfo.get("name", decoded_id_token.get("name")),
            picture=userinfo.get("picture", decoded_id_token.get("picture")),
            aud=decoded_id_token.get("aud"),
            iss=decoded_id_token.get("iss"),
            exp=decoded_id_token.get("exp"),
            iat=decoded_id_token.get("iat"),
            custom_claims={k: v for k, v in userinfo.items() if k not in UserProfile.__annotations__ and k != "sub"}
        )
        return profile
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Failed to fetch user profile: {e}. Response: {e.response.text}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching user profile: {e}")
