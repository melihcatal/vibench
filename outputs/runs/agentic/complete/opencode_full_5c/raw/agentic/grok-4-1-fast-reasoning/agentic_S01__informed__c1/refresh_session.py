from identity_client import get_cognito_client, COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID
from identity_models import parse_auth_response, build_refresh_params


def refresh_session(refresh_token: str) -> dict:
    client = get_cognito_client()
    resp = client.admin_initiate_auth(
        UserPoolId=COGNITO_USER_POOL_ID,
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters=build_refresh_params(refresh_token),
    )
    return parse_auth_response(resp)
