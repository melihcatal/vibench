import jwt
import requests

from identity_models import normalize_profile_claims


def profile_claims(payload, config=None):
    config = config or {}
    issuer = config.get("issuer") or f"https://cognito-idp.{config.get('region', 'us-east-1')}.amazonaws.com/{config.get('user_pool_id', '')}"
    jwks = requests.get(issuer.rstrip("/") + "/.well-known/jwks.json", timeout=15).json()
    claims = jwt.decode(payload["id_token"], options={"verify_signature": False}, algorithms=["RS256"], audience=config.get("client_id"), issuer=issuer)
    return normalize_profile_claims(claims)
