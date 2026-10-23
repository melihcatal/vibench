from __future__ import annotations

from typing import Optional

from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import DEFAULT_OUTPUT_TYPE, get_content_safety_client
from safety_models import SafetyDecision, normalize_category_scores


def moderate_text(text: str, blocklist_name: Optional[str] = None) -> SafetyDecision:
    client = get_content_safety_client()
    response = client.analyze_text(
        AnalyzeTextOptions(
            text=text,
            output_type=DEFAULT_OUTPUT_TYPE,
            blocklist_names=[blocklist_name] if blocklist_name else None,
        )
    )
    categories = normalize_category_scores([item.as_dict() for item in response.categories_analysis])
    block_reasons = [name for name, score in categories.items() if (score.severity or 0) >= 2]
    return SafetyDecision(
        text=text,
        allowed=len(block_reasons) == 0,
        categories=categories,
        block_reasons=block_reasons,
        metadata={
            "provider_endpoint": client._endpoint,
            "service": "Azure AI Content Safety",
        },
    )
