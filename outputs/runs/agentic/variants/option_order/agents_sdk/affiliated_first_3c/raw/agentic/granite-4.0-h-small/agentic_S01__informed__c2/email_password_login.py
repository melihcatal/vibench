import os
import idaas_eiam
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse

# Configure client using environment variables
CLIENT_ID = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
CLIENT_SECRET = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
ENDPOINT = os.getenv('ALIBABA_CLOUD_IDENTITY_ENDPOINT', 'https://idaas.cn-north-1.alibabacloud.com')

client = idaas_eiam.IdentityClient(endpoint=ENDPOINT, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

def email_password_login(email: str, password: str) -> EmailPasswordLoginResponse:
    """Sign in a user with email and password using Alibaba Cloud IDaaS EIAM.

    Returns an access token and refresh token for the authenticated session.
    """
    payload = EmailPasswordLoginRequest(
        username=email,
        password=password,
    )
    response = client.email_password_login(payload)
    return response
