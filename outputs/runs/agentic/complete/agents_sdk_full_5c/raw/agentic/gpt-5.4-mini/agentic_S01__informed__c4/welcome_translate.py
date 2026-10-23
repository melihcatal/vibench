from __future__ import annotations

from identity_client import get_identity_client
from identity_models import TranslationRequest


def welcome_translate(text: str, target_locale: str, source_locale: str | None = None):
    client = get_identity_client()
    request = TranslationRequest(text=text, target_locale=target_locale, source_locale=source_locale)
    return client.translate_copy(request)
