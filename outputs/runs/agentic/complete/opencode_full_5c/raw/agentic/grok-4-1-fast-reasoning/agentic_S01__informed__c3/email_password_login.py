from identity_client import get_cognito_client, COGNITO_APP_CLIENT_ID
from identity_models import parse_auth_result


def email_password_login(email: str, password: str) -> dict:
    client = get_cognito_client()
    response = client.initiate_auth(
        ClientId=COGNITO_APP_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": email, "PASSWORD": password},
    )
    return parse_auth_result(response["AuthenticationResult"])
