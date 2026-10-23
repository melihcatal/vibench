from identity_client import get_cognito_client, COGNITO_USER_POOL_ID
from identity_models import build_user_attributes, parse_register_response


def register_user(email: str, password: str) -> dict:
    client = get_cognito_client()
    resp = client.admin_create_user(
        UserPoolId=COGNITO_USER_POOL_ID,
        Username=email,
        UserAttributes=build_user_attributes(email),
        TemporaryPassword=password,
        MessageAction="SUPPRESS",
    )
    client.admin_set_user_password(
        UserPoolId=COGNITO_USER_POOL_ID,
        Username=email,
        Password=password,
        Permanent=True,
    )
    return parse_register_response(resp)
