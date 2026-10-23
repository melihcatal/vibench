from identity_client import cognito_client, USER_POOL_ID, APP_CLIENT_ID
from identity_models import RefreshRequest, AuthTokens


def refresh_session(req: RefreshRequest) -> AuthTokens:
    response = cognito_client.admin_initiate_auth(
        UserPoolId=USER_POOL_ID,
        ClientId=APP_CLIENT_ID,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": req.refresh_token},
    )
    auth_result = response["AuthenticationResult"]
    return AuthTokens(
        access_token=auth_result["AccessToken"],
        id_token=auth_result["IdToken"],
        refresh_token=auth_result.get("RefreshToken"),
        expires_in=auth_result["ExpiresIn"],
    )
