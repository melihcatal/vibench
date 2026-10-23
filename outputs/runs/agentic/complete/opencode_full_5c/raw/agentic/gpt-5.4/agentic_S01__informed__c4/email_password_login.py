from identity_client import COGNITO_PROVIDER, get_cognito_client, get_cognito_client_id
from identity_models import LoginRequest, TokenSet


def email_password_login(email: str, password: str) -> dict:
    request = LoginRequest(email=email, password=password)
    client = get_cognito_client()
    response = client.initiate_auth(
        ClientId=get_cognito_client_id(),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": request.email, "PASSWORD": request.password},
    )
    auth_result = response["AuthenticationResult"]
    tokens = TokenSet(
        provider=COGNITO_PROVIDER,
        access_token=auth_result["AccessToken"],
        refresh_token=auth_result.get("RefreshToken"),
        id_token=auth_result.get("IdToken"),
        token_type=auth_result.get("TokenType"),
        expires_in=auth_result.get("ExpiresIn"),
    )
    return tokens.to_dict()
