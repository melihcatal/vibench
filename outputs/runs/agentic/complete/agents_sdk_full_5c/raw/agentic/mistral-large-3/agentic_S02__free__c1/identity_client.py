import os
from typing import TypedDict

class IdentityConfig(TypedDict):
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_DOMAIN: str

def get_identity_config() -> IdentityConfig:
    return {
        "AUTH0_CLIENT_ID": os.getenv("AUTH0_CLIENT_ID"),
        "AUTH0_CLIENT_SECRET": os.getenv("AUTH0_CLIENT_SECRET"),
        "AUTH0_DOMAIN": os.getenv("AUTH0_DOMAIN", "dev-12345678.us.auth0.com"),
    }