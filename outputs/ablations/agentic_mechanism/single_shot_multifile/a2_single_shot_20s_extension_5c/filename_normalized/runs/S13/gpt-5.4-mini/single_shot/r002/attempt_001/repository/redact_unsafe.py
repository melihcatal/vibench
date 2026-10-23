from typing import Any, Dict, List, Optional
from openai import OpenAI
from safety_client import get_openai_client, get_moderation_model
from safety_models import redact_spans_from_moderation, normalize_text_input


def redact_unsafe(text: str, client: Optional[OpenAI] = None, model: Optional[str] = None) -> Dict[str, Any]:
    client = client or get_openai_client()
    model = model or get_moderation_model()
    payload = normalize_text_input(text)
    resp = client.moderations.create(model=model, input=payload)
    return redact_spans_from_moderation(resp, text=payload)
