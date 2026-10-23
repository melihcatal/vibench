from identity_client import get_identity_client, get_app_client_id
from identity_models import AuthTokens


def login_with_email_password(email: str, password: str) -> AuthTokens:
    client = get_identity_client()
    app_client_id = get_app_client_id()

    response = client.initiate_auth(
        ClientId=app_client_id,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password,
        },
    )
    auth_result = response["AuthenticationResult"]
    return AuthTokens(
        access_token=auth_result["AccessToken"],
        refresh_token=auth_result["RefreshToken"],
        id_token=auth_result["IdToken"],
    )
