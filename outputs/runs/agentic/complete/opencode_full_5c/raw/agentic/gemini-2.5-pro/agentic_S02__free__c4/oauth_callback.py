import httpx
from identity_client import get_identity_config
from identity_models import OAuthTokenResponse


async def exchange_okta_code_for_token(
    code: str, redirect_uri: str
) -> OAuthTokenResponse:
    config = get_identity_config()
    token_url = f"https://{config.OKTA_DOMAIN}/oauth2/default/v1/token"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": config.OKTA_CLIENT_ID,
        "client_secret": config.OKTA_CLIENT_SECRET,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=payload, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        return OAuthTokenResponse(**token_data)


if __name__ == "__main__":
    # This is not example usage, it's for verification
    # A real application would get the code from the callback request
    import asyncio

    async def main():
        # This is a placeholder code, it will not work without a real auth flow
        fake_code = "dummy_code_for_testing"
        try:
            token_response = await exchange_okta_code_for_token(
                fake_code, "http://localhost:8080/callback"
            )
            print("Token response:", token_response.model_dump_json(indent=2))
        except httpx.HTTPStatusError as e:
            print(f"Failed to exchange code: {e.response.status_code}")
            print(e.response.text)

    asyncio.run(main())
