from identity_client import oidc_session, userinfo_url
from identity_models import normalize_claims


def fetch_profile(access_token: str):
    session = oidc_session(
        redirect_uri="https://localhost/callback", scope=["openid", "profile", "email"]
    )
    session.token = {"access_token": access_token, "token_type": "Bearer"}
    claims = session.get(userinfo_url()).json()
    return normalize_claims(claims)
