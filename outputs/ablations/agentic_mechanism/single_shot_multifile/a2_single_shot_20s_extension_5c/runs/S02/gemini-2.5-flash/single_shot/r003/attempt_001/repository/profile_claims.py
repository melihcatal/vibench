import requests
import jwt
from identity_models import UserInfo, normalize_google_user_info

def fetch_google_profile_claims(access_token: str) -> UserInfo:
    userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    profile_data = response.json()
    return normalize_google_user_info(profile_data)

def decode_id_token_claims(id_token: str) -> UserInfo:
    decoded_token = jwt.decode(id_token, options={"verify_signature": False})
    return normalize_google_user_info(decoded_token)
