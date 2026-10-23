from typing import Any, Dict, Optional
from openai import OpenAI
from safety_client import get_openai_client, get_moderation_model, get_thresholds
from safety_models import threshold_decision_from_moderation, normalize_text_input


def safety_threshold(text: str, client: Optional[OpenAI] = None, model: Optional[str] = None, thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    client = client or get_openai_client()
    model = model or get_moderation_model()
    payload = normalize_text_input(text)
    resp = client.moderations.create(model=model, input=payload)
    return threshold_decision_from_moderation(resp, text=payload, thresholds=thresholds or get_thresholds())
