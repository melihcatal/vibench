from __future__ import annotations

from identity_client import get_identity_client
from identity_models import ModerationRequest


def profile_moderation(text: str, user_id: str | None = None, locale: str | None = None):
    client = get_identity_client()
    request = ModerationRequest(text=text, user_id=user_id, locale=locale)
    return client.moderate_profile(request)
