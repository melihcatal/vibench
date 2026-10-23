from __future__ import annotations

from typing import Any, Dict

from safety_client import analyze_text
from safety_models import SafetyRequest, to_serializable_result


def moderate_text(
    text: str, language: str = "en", user_id: str | None = None
) -> Dict[str, Any]:
    result = analyze_text(SafetyRequest(text=text, language=language, user_id=user_id))
    return to_serializable_result(result)
