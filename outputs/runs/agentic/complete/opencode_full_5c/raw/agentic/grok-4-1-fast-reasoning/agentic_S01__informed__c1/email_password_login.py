from identity_client import get_cognito_client, COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID
from identity_models import parse_auth_response, build_admin_auth_params


def email_password_login(email: str, password: str) -> dict:
    client = get_cognito_client()
    resp = client.admin_initiate_auth(
        UserPoolId=COGNITO_USER_POOL_ID,
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters=build_admin_auth_params(email, password),
    )
    return parse_auth_response(resp)
