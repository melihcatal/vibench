from typing import Any, Dict, Optional
from openai import OpenAI
from safety_client import build_openai_client, provider_name, get_category_thresholds
from safety_models import build_threshold_result, extract_moderation_output, threshold_decision

MODEL = "omni-moderation-latest"


def safety_threshold(text: str, thresholds: Optional[Dict[str, float]] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_openai_client()
    response = client.moderations.create(model=MODEL, input=text)
    parsed = extract_moderation_output(response)
    effective_thresholds = thresholds or get_category_thresholds()
    decision = threshold_decision(parsed.get("category_scores", {}), effective_thresholds)
    return build_threshold_result(
        provider=provider_name(),
        operation="safety_threshold",
        input_text=text,
        moderation=parsed,
        thresholds=effective_thresholds,
        decision=decision,
        metadata=metadata,
    )
