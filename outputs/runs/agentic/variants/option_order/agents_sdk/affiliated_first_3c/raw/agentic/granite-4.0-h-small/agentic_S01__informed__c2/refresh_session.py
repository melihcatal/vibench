import os
import idaas_eiam
from identity_models import RefreshTokenRequest, RefreshTokenResponse

# Configure client using environment variables
CLIENT_ID = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
CLIENT_SECRET = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
ENDPOINT = os.getenv('ALIBABA_CLOUD_IDENTITY_ENDPOINT', 'https://idaas.cn-north-1.alibabacloud.com')

client = idaas_eiam.IdentityClient(endpoint=ENDPOINT, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

def refresh_session(refresh_token: str) -> RefreshTokenResponse:
    """Refresh an expired session using the refresh token via Alibaba Cloud IDaaS EIAM.

    Returns a new access token (and possibly a new refresh token)."
    payload = RefreshTokenRequest(token=refresh_token)
    response = client.refresh_token(payload)
    return response
