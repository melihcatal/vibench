import httpx
from identity_client import get_identity_config
from identity_models import NormalizedProfile


async def fetch_okta_user_profile(access_token: str) -> NormalizedProfile:
    """
    Fetches user profile claims from Okta's userinfo endpoint.
    """
    config = get_identity_config()
    userinfo_endpoint = f"https://{config['okta_domain']}/oauth2/v1/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(userinfo_endpoint, headers=headers)
        response.raise_for_status()
        claims = response.json()

    return NormalizedProfile(
        id=claims.get("sub"),
        name=claims.get("name"),
        email=claims.get("email"),
        username=claims.get("preferred_username"),
        picture=claims.get("picture"),
        raw_claims=claims,
    )
