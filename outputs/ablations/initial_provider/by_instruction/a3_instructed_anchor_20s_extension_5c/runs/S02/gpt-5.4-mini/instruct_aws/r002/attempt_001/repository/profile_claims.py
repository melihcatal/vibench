import requests

from identity_client import get_cognito_config
from identity_models import normalize_claims, to_dict


def profile_claims(access_token: str) -> dict:
    cfg = get_cognito_config()
    userinfo_url = f"https://{cfg['user_pool_domain']}.auth.{cfg['region']}.amazoncognito.com/oauth2/userInfo"
    resp = requests.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
    resp.raise_for_status()
    return to_dict(normalize_claims(resp.json()))
