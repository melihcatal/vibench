import os
from typing import Any, Dict, Optional
from openai import OpenAI
from safety_client import get_openai_client, get_moderation_model
from safety_models import moderation_decision_from_openai, normalize_text_input


def moderate_text(text: str, client: Optional[OpenAI] = None, model: Optional[str] = None) -> Dict[str, Any]:
    client = client or get_openai_client()
    model = model or get_moderation_model()
    payload = normalize_text_input(text)
    resp = client.moderations.create(model=model, input=payload)
    return moderation_decision_from_openai(resp, text=payload)
