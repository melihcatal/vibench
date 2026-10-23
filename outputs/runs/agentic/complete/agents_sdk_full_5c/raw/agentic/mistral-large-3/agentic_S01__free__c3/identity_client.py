import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class IdentityConfig:
    firebase_project_id: Optional[str] = os.getenv("FIREBASE_PROJECT_ID")
    firebase_api_key: Optional[str] = os.getenv("FIREBASE_API_KEY")
    firebase_private_key: Optional[str] = os.getenv("FIREBASE_PRIVATE_KEY")
    firebase_client_email: Optional[str] = os.getenv("FIREBASE_CLIENT_EMAIL")


def load_identity_config() -> IdentityConfig:
    return IdentityConfig()