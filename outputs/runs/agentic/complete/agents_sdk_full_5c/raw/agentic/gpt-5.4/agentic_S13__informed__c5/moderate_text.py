from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from safety_client import AzureContentSafetyClient
from safety_models import as_decision_dict, normalize_analysis_result


def moderate_text(
    text: str,
    categories: Optional[Iterable[str]] = None,
    blocklist_names: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    client = AzureContentSafetyClient()
    response_json = client.analyze_text(
        text=text,
        categories=categories,
        blocklist_names=blocklist_names,
    )
    result = normalize_analysis_result(text, response_json)
    return as_decision_dict(result)
