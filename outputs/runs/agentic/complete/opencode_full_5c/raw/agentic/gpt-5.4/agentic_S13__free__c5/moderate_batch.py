from __future__ import annotations

from collections.abc import Iterable

from moderate_text import moderate_text
from safety_models import SafetyResult


def moderate_batch(
    messages: Iterable[str], language: str | None = None
) -> list[SafetyResult]:
    return [moderate_text(text=message, language=language) for message in messages]
