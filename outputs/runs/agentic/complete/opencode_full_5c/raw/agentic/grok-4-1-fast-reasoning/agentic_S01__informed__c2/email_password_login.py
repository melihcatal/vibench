from identity_client import cognito_client, USER_POOL_ID, APP_CLIENT_ID
from identity_models import LoginRequest, AuthTokens


def email_password_login(req: LoginRequest) -> AuthTokens:
    response = cognito_client.admin_initiate_auth(
        UserPoolId=USER_POOL_ID,
        ClientId=APP_CLIENT_ID,
        AuthFlow="ADMIN_USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": req.email, "PASSWORD": req.password},
    )
    auth_result = response["AuthenticationResult"]
    return AuthTokens(
        access_token=auth_result["AccessToken"],
        id_token=auth_result["IdToken"],
        refresh_token=auth_result.get("RefreshToken"),
        expires_in=auth_result["ExpiresIn"],
    )
