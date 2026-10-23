import os
from identity_client import IdentityClient
from identity_models import RegisterRequest, RegisterResponse

# Alibaba Cloud IDaaS EIAM
client = IdentityClient(
    service='idaas_eiam',
    region=os.getenv('ALIBABA_CLOUD_REGION', 'cn-hangzhou'),
    access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
)

async def register_user(email: str, password: str) -> RegisterResponse:
    # Normalize payload
    payload = RegisterRequest.from_dict({
        "email": email,
        "password": password,
    })
    # Call Alibaba Cloud IDaaS EIAM SDK
    response = await client.register(payload)
    # Convert to local model
    return RegisterResponse.from_dict(response.dict())
