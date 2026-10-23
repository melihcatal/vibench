from __future__ import annotations

from typing import Any, Dict, Iterable, List

from safety_client import analyze_batch
from safety_models import SafetyRequest, to_serializable_result


def moderate_batch(messages: Iterable[Dict[str, str]]) -> List[Dict[str, Any]]:
    requests_ = [
        SafetyRequest(
            text=item["text"],
            language=item.get("language", "en"),
            user_id=item.get("user_id"),
        )
        for item in messages
    ]
    return [to_serializable_result(result) for result in analyze_batch(requests_)]
