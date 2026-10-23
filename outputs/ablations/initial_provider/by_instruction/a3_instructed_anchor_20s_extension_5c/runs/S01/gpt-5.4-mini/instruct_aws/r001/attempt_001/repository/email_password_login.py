from identity_client import cognito_idp_client, load_identity_config
from identity_models import LoginRequest, normalize_email, to_payload


def email_password_login(email: str, password: str):
    config = load_identity_config()
    client = cognito_idp_client()
    payload = to_payload(LoginRequest(email=normalize_email(email), password=password))
    response = client.initiate_auth(
        ClientId=config.client_id,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": payload["email"], "PASSWORD": payload["password"]},
    )
    result = response.get("AuthenticationResult", {})
    return {
        "access_token": result.get("AccessToken"),
        "id_token": result.get("IdToken"),
        "refresh_token": result.get("RefreshToken"),
        "expires_in": result.get("ExpiresIn"),
        "token_type": result.get("TokenType"),
    }
