import requests
from identity_client import get_oauth_config
from identity_models import NormalizedProfile

def fetch_normalized_profile(provider_name: str, access_token: str) -> NormalizedProfile:
    config = get_oauth_config(provider_name)
    if not config:
        raise ValueError(f"Unsupported provider: {provider_name}")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(config['userinfo_url'], headers=headers)
    response.raise_for_status()
    userinfo = response.json()

    # Normalize Google OIDC claims
    if provider_name == "google":
        return NormalizedProfile(
            sub=userinfo.get("sub"),
            name=userinfo.get("name"),
            given_name=userinfo.get("given_name"),
            family_name=userinfo.get("family_name"),
            email=userinfo.get("email"),
            email_verified=userinfo.get("email_verified"),
            picture=userinfo.get("picture"),
            locale=userinfo.get("locale"),
            provider=provider_name,
        )
    # Normalize Microsoft Graph claims
    elif provider_name == "microsoft":
        return NormalizedProfile(
            sub=userinfo.get("id"),
            name=userinfo.get("displayName"),
            given_name=userinfo.get("givenName"),
            family_name=userinfo.get("surname"),
            email=userinfo.get("userPrincipalName"),
            email_verified=None,
            picture=userinfo.get("photo"),
            locale=userinfo.get("preferredLanguage"),
            provider=provider_name,
        )
    else:
        raise ValueError(f"Unsupported provider for normalization: {provider_name}")