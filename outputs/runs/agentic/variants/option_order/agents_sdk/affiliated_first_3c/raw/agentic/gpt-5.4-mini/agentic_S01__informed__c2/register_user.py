from __future__ import annotations

from typing import Any

from identity_client import Auth0IdentityClient
from identity_models import EmailPasswordIdentityRequest, LifecycleResult

# Auth0 Management API / Authentication API integration

def register_user(request: EmailPasswordIdentityRequest) -> LifecycleResult:
    client = Auth0IdentityClient()
    payload: dict[str, Any] = {
        "email": request.normalized_email(),
        "password": request.password or "",
        "name": request.display_name,
        "metadata": request.metadata,
    }
    created = client.register_user(**payload)
    return LifecycleResult(success=True, message="User registered", data=created)
