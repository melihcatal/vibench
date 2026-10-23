from identity_client import load_config, userinfo
from identity_models import ClaimsProfile, normalize_claims


def profile_claims(access_token: str) -> ClaimsProfile:
    config = load_config()
    claims = normalize_claims(userinfo(config.auth0_domain, access_token))
    return ClaimsProfile(
        subject=claims.get("sub", ""),
        email=claims.get("email"),
        name=claims.get("name"),
        issuer=claims.get("iss"),
        raw=claims,
    )
