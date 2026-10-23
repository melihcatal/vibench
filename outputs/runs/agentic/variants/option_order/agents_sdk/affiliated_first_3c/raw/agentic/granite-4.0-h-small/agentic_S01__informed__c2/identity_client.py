import os
from typing import Generic, TypeVar

# Choose one concrete provider implementation based on env vars (fallback to Alibaba IDaaS EIAM)
SERVICE = os.getenv('IDENTITY_PROVIDER', 'ALIBABA_IDAAS')

if SERVICE == 'ALIBABA_IDAAS':
    import idaas_eiam
    from identity_models import (
        UserCreationRequest,
        UserCreationResponse,
        EmailPasswordLoginRequest,
        EmailPasswordLoginResponse,
        RefreshTokenRequest,
        RefreshTokenResponse,
        InitiatePasswordResetRequest,
        InitiatePasswordResetResponse,
    )

    class IdentityClient:
        def __init__(self, endpoint: str, client_id: str, client_secret: str):
            self.client = idaas_eiam.IdentityClient(
                endpoint=endpoint,
                client_id=client_id,
                client_secret=client_secret,
            )
        
        def register_user(self, payload: UserCreationRequest) -> UserCreationResponse:
            return self.client.register_user(payload)
        
        def email_password_login(self, payload: EmailPasswordLoginRequest) -> EmailPasswordLoginResponse:
            return self.client.email_password_login(payload)
        
        def refresh_token(self, payload: RefreshTokenRequest) -> RefreshTokenResponse:
            return self.client.refresh_token(payload)
        
        def initiate_password_reset(self, payload: InitiatePasswordResetRequest) -> InitiatePasswordResetResponse:
            return self.client.initiate_password_reset(payload)
else:
    raise RuntimeError('Unsupported identity provider')
