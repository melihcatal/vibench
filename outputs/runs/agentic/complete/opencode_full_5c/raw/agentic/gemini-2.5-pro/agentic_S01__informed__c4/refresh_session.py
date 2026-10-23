from identity_client import get_identity_client, get_app_client_id
from identity_models import AuthTokens


def refresh_user_session(refresh_token: str) -> AuthTokens:
    client = get_identity_client()
    app_client_id = get_app_client_id()

    response = client.initiate_auth(
        ClientId=app_client_id,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={
            "REFRESH_TOKEN": refresh_token,
        },
    )
    auth_result = response["AuthenticationResult"]
    new_refresh_token = auth_result.get("RefreshToken", refresh_token)
    return AuthTokens(
        access_token=auth_result["AccessToken"],
        refresh_token=new_refresh_token,
        id_token=auth_result["IdToken"],
    )
