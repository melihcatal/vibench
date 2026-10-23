import os
import idaas_eiam
from identity_models import InitiatePasswordResetRequest, InitiatePasswordResetResponse

# Configure client using environment variables
CLIENT_ID = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
CLIENT_SECRET = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
ENDPOINT = os.getenv('ALIBABA_CLOUD_IDENTITY_ENDPOINT', 'https://idaas.cn-north-1.alibabacloud.com')

client = idaas_eiam.IdentityClient(endpoint=ENDPOINT, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

def password_reset(email: str) -> InitiatePasswordResetResponse:
    """Start a password reset flow for a local account via Alibaba Cloud IDaaS EIAM.

    Sends a reset link / verification code to the user's registered email.
    """
    payload = InitiatePasswordResetRequest(username=email)
    response = client.initiate_password_reset(payload)
    return response
