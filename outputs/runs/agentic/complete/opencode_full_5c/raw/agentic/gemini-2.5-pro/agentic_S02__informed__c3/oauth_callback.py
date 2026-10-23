from identity_client import get_identity_client
from identity_models import TokenResponse


def exchange_code_for_token(authorization_code: str):
    client = get_identity_client()

    token_data = client.auth0.get_token(
        grant_type="authorization_code",
        code=authorization_code,
        redirect_uri=client.callback_url,
    )

    return TokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        scope=token_data.get("scope"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
