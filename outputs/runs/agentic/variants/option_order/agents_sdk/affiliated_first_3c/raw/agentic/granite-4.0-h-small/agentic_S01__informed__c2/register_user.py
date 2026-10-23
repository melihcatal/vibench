import os
import idaas_eiam
from identity_models import UserCreationRequest, UserCreationResponse

# Configure client using environment variables
CLIENT_ID = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
CLIENT_SECRET = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
ENDPOINT = os.getenv('ALIBABA_CLOUD_IDENTITY_ENDPOINT', 'https://idaas.cn-north-1.alibabacloud.com')

client = idaas_eiam.IdentityClient(endpoint=ENDPOINT, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

def register_user(email: str, password: str) -> UserCreationResponse:
    """Create a new local email/password user account via Alibaba Cloud IDaaS EIAM.

    Returns the server response containing the user ID and initial session token.
    """
    payload = UserCreationRequest(
        username=email,
        password=password,
    )
    # The SDK serialises payload to the expected JSON shape for the RegisterUser API
    response = client.register_user(payload)
    return response
