from identity_client import get_cognito_client, COGNITO_APP_CLIENT_ID
from identity_models import parse_auth_result


def refresh_session(refresh_token: str) -> dict:
    client = get_cognito_client()
    response = client.initiate_auth(
        ClientId=COGNITO_APP_CLIENT_ID,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": refresh_token},
    )
    return parse_auth_result(response["AuthenticationResult"])
