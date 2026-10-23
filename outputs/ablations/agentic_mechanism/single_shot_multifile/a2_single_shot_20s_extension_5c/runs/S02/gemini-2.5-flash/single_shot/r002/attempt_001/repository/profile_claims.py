import jwt
import requests
from identity_client import GOOGLE_USERINFO_URL
from identity_models import UserClaims

def fetch_google_user_claims(id_token: str, access_token: str = None) -> UserClaims:
    claims_data = {}
    
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
            userinfo_response.raise_for_status()
            claims_data = userinfo_response.json()
        except requests.exceptions.RequestException:
            pass
    
    if not claims_data and id_token:
        try:
            claims_data = jwt.decode(id_token, options={"verify_signature": False})
        except jwt.exceptions.DecodeError as e:
            raise ValueError(f"Invalid ID token: {e}")

    if not claims_data:
        raise ValueError("No claims data could be retrieved from ID token or UserInfo endpoint.")

    sub = claims_data.get("sub")
    email = claims_data.get("email")
    name = claims_data.get("name")

    return UserClaims(sub=sub, email=email, name=name, **claims_data)