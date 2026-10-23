import os
from typing import Any, Dict, Optional
from openai import OpenAI
from safety_client import build_openai_client, provider_name
from safety_models import build_moderation_result, extract_moderation_output

MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_text(text: str, input_type: str = "text", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_openai_client()
    response = client.moderations.create(model=MODEL, input=text)
    parsed = extract_moderation_output(response)
    result = build_moderation_result(
        provider=provider_name(),
        operation="moderate_text",
        input_text=text,
        input_type=input_type,
        moderation=parsed,
        metadata=metadata,
    )
    return result
