from __future__ import annotations

from identity_client import IdentityClient
from identity_models import EmailPasswordAccountRequest


def register_user(email: str, password: str, display_name: str | None = None, locale: str | None = None):
    client = IdentityClient()
    request = EmailPasswordAccountRequest(email=email, password=password, display_name=display_name, locale=locale)
    return client.register_user(request)
