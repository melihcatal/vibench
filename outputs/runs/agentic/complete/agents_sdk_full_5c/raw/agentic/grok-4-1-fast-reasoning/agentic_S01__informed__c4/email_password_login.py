from identity_client import get_cognito_client
from identity_models import build_auth_payload

def email_password_login(email: str, password: str):
    client = get_cognito_client()
    payload = build_auth_payload("ADMIN_USER_PASSWORD_AUTH", email=email, password=password)
    response = client.admin_initiate_auth(**payload)
    return response["AuthenticationResult"]