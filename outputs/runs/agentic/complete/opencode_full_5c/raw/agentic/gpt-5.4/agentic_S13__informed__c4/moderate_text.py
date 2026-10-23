from __future__ import annotations

from typing import Any

from safety_client import analyze_text
from safety_models import SafetyRequest, result_to_dict


def moderate_text(
    text: str, language: str | None = None, user_id: str | None = None
) -> dict[str, Any]:
    result = analyze_text(SafetyRequest(text=text, language=language, user_id=user_id))
    return result_to_dict(result)
