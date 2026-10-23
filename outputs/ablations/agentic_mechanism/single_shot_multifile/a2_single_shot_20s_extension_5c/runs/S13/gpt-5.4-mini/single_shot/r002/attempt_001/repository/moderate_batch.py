from typing import Any, Dict, List, Optional
from openai import OpenAI
from safety_client import get_openai_client, get_moderation_model
from safety_models import batch_moderation_from_openai, normalize_text_list


def moderate_batch(messages: List[str], client: Optional[OpenAI] = None, model: Optional[str] = None) -> Dict[str, Any]:
    client = client or get_openai_client()
    model = model or get_moderation_model()
    payload = normalize_text_list(messages)
    resp = client.moderations.create(model=model, input=payload)
    return batch_moderation_from_openai(resp, messages=payload)
