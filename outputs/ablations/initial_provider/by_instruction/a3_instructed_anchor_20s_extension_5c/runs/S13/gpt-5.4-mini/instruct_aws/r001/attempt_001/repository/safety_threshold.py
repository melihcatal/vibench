from typing import Any, Dict

from moderate_text import moderate_text


def safety_threshold(text: str, thresholds: Dict[str, Any] | None = None) -> bool:
    return moderate_text(text, thresholds=thresholds).allowed
