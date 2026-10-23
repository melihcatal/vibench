import httpx
from identity_client import get_identity_config
from identity_models import UserProfile


async def get_okta_user_profile(access_token: str) -> UserProfile:
    config = get_identity_config()
    userinfo_url = f"https://{config.OKTA_DOMAIN}/oauth2/default/v1/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(userinfo_url, headers=headers)
        response.raise_for_status()
        claims = response.json()

        # Normalize claims into a standard UserProfile model
        return UserProfile(
            id=claims.get("sub"),
            name=claims.get("name"),
            email=claims.get("email"),
            raw_claims=claims,
        )


if __name__ == "__main__":
    # This is not an example, it's for verification.
    # A real application would get the access token from the session after login.
    import asyncio

    async def main():
        # This is a placeholder token, it will not work.
        fake_token = "dummy_token"
        try:
            profile = await get_okta_user_profile(fake_token)
            print("User profile:", profile.model_dump_json(indent=2))
        except httpx.HTTPStatusError as e:
            print(f"Failed to fetch profile: {e.response.status_code}")
            print(e.response.text)

    asyncio.run(main())
