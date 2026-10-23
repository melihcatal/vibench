import os
import json
from pydantic import BaseSettings

class IdentitySettings(BaseSettings):
    # Auth0 configuration (same-scenario OAuth/OIDC)
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('AUTH0_REDIRECT_URI')

    # Azure AD B2C (PKCE scenario)
    TENANT_ID = os.getenv('AZURE_TENANT_ID')
    AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')

    class Config:
        env_file = '.env'

    def __post_init__(self):
        for k in self.__dict__:
            if not getattr(self, k):
                raise RuntimeError(f'Missing environment variable: {k}')

class IdentityClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = IdentitySettings().dict()
        return cls._instance

    @classmethod
    def from_env(cls):
        return cls()
