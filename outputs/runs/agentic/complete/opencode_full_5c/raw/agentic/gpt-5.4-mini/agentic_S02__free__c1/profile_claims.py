from identity_client import create_oauth_session, load_identity_provider_config
from identity_models import NormalizedClaims, normalize_claims


def profile_claims(access_token: str) -> NormalizedClaims:
    config = load_identity_provider_config("OIDC")
    session = create_oauth_session(config)
    response = session.get(
        config.userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"}
    )
    response.raise_for_status()
    return normalize_claims(config.issuer, response.json())
