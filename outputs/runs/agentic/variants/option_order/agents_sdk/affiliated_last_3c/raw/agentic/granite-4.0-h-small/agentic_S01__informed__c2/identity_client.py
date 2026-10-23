import os
from botocore.exceptions import ClientError

# -------------------------------------------------
# Local configuration helpers for Email/Password flow
# -------------------------------------------------

def get_aws_credentials():
    """Load AWS credentials from environment or local config."""
    region = os.getenv('AWS_REGION', 'us-east-1')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    return {
        'region_name': region,
        'aws_access_key_id': access_key,
        'aws_secret_access_key': secret_key,
    }

def init_cognito_client(user_pool_id='YOUR_USER_POOL_ID', client_id='YOUR_CLIENT_ID'):
    """Create a pre-configured boto3 Cognito client."""
    creds = get_aws_credentials()
    return boto3.client('cognito-idp', **creds)

def _handle_error(err):
    raise RuntimeError(f"Cognito failure: {err}")

# Public client utility
client = init_cognito_client()

# Convenience wrappers (can be called from other modules)
def signup_user(email, password):
    return client.sign_up(ClientId=client_id, Username=email, Password=password)

def confirm_signup(email, code):
    return client.confirm_sign_up(ClientId=client_id, Username=email, ConfirmationCode=code)

def authenticate(email, password):
    try:
        resp = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': email, 'PASSWORD': password}
        )
        return resp
    except ClientError as exc:
        _handle_error(exc)

def refresh_token(refresh_token):
    try:
        resp = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={'REFRESH_TOKEN': refresh_token}
        )
        return resp
    except ClientError as exc:
        _handle_error(exc)
