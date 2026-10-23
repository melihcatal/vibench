from identity_client import COGNITO_PROVIDER, get_cognito_client, get_cognito_client_id
from identity_models import RefreshSessionRequest, TokenSet


def refresh_session(refresh_token: str) -> dict:
    request = RefreshSessionRequest(refresh_token=refresh_token)
    client = get_cognito_client()
    response = client.initiate_auth(
        ClientId=get_cognito_client_id(),
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": request.refresh_token},
    )
    auth_result = response["AuthenticationResult"]
    tokens = TokenSet(
        provider=COGNITO_PROVIDER,
        access_token=auth_result["AccessToken"],
        refresh_token=request.refresh_token,
        id_token=auth_result.get("IdToken"),
        token_type=auth_result.get("TokenType"),
        expires_in=auth_result.get("ExpiresIn"),
    )
    return tokens.to_dict()
