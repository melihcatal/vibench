from __future__ import annotations

from observability_client import client


def dashboard_note_translate(text: str, target_locale: str, source_locale: str = "en"):
    return client().translate(text, target_locale=target_locale, source_locale=source_locale)
