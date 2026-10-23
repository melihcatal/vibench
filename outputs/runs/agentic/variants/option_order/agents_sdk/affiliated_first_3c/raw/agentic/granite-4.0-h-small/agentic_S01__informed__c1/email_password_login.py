import os
from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse

# Alibaba Cloud IDaaS EIAM
client = IdentityClient(
    service='idaas_eiam',
    region=os.getenv('ALIBABA_CLOUD_REGION', 'cn-hangzhou'),
    access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
)

async def email_password_login(email: str, password: str) -> LoginResponse:
    # Normalize payload
    payload = LoginRequest.from_dict({
        "email": email,
        "password": password,
    })
    # Call Alibaba Cloud IDaaS EIAM SDK
    response = await client.login_email_password(payload)
    # Convert to local model
    return LoginResponse.from_dict(response.dict())
