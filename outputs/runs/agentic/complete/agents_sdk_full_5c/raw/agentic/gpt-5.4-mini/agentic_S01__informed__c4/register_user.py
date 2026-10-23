from __future__ import annotations

from identity_client import get_identity_client
from identity_models import EmailPasswordIdentityRequest


def register_user(email: str, password: str, display_name: str | None = None, metadata: dict | None = None):
    client = get_identity_client()
    request = EmailPasswordIdentityRequest(email=email, password=password, display_name=display_name, metadata=metadata or {})
    return client.register_user(request)
