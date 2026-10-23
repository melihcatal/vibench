from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from safety_client import AzureContentSafetyClient
from safety_models import as_decision_dict, normalize_analysis_result


def moderate_batch(
    messages: Iterable[str],
    categories: Optional[Iterable[str]] = None,
    blocklist_names: Optional[Iterable[str]] = None,
) -> List[Dict[str, Any]]:
    client = AzureContentSafetyClient()
    decisions: List[Dict[str, Any]] = []
    for text in messages:
        response_json = client.analyze_text(
            text=text,
            categories=categories,
            blocklist_names=blocklist_names,
        )
        decisions.append(as_decision_dict(normalize_analysis_result(text, response_json)))
    return decisions
