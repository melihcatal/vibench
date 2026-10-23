import os
from identity_client import IdentityClient
from identity_models import RefreshRequest, RefreshResponse

# Alibaba Cloud IDaaS EIAM
client = IdentityClient(
    service='idaas_eiam',
    region=os.getenv('ALIBABA_CLOUD_REGION', 'cn-hangzhou'),
    access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
)

async def refresh_session(refresh_token: str) -> RefreshResponse:
    # Normalize payload
    payload = RefreshRequest.from_dict({
        "refresh_token": refresh_token,
    })
    # Call Alibaba Cloud IDaaS EIAM SDK
    response = await client.refresh_token(payload)
    # Convert to local model
    return RefreshResponse.from_dict(response.dict())
