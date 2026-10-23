from __future__ import annotations

from typing import Iterable, List

from moderate_text import moderate_text
from safety_models import ModerationResult


def moderate_batch(
    messages: Iterable[str], language: str = "en"
) -> List[ModerationResult]:
    return [moderate_text(message, language=language) for message in messages]
