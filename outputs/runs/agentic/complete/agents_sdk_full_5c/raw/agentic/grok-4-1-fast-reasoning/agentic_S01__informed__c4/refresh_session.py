from identity_client import get_cognito_client
from identity_models import build_auth_payload

def refresh_session(refresh_token: str):
    client = get_cognito_client()
    payload = build_auth_payload("REFRESH_TOKEN_AUTH", refresh_token=refresh_token)
    response = client.admin_initiate_auth(**payload)
    return response["AuthenticationResult"]