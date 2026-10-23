import os
from identity_client import IdentityClient
from identity_models import ResetRequest, ResetResponse

# Alibaba Cloud IDaaS EIAM
client = IdentityClient(
    service='idaas_eiam',
    region=os.getenv('ALIBABA_CLOUD_REGION', 'cn-hangzhou'),
    access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
)

def start_password_reset(email: str) -> ResetResponse:
    # Normalize payload (password reset does not require password yet)
    payload = ResetRequest.from_dict({
        "email": email,
    })
    # Call Alibaba Cloud IDaaS EIAM SDK (reset initiation)
    response = client.start_password_reset(payload)
    return ResetResponse.from_dict(response.dict())
