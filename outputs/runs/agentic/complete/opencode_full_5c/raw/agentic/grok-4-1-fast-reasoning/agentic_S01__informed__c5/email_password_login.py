from identity_client import cognito_client, APP_CLIENT_ID
from identity_models import LoginRequest, parse_auth_result


def email_password_login(req: LoginRequest) -> dict:
    """
    Signs in a user with email and password using Amazon Cognito User Pools and returns tokens.
    """
    response = cognito_client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=APP_CLIENT_ID,
        AuthParameters={"USERNAME": req["email"], "PASSWORD": req["password"]},
    )
    return parse_auth_result(response)
