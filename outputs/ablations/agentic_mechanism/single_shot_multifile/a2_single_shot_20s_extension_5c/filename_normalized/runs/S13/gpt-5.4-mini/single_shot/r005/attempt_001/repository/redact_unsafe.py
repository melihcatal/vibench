from typing import Any, Dict, Optional
from openai import OpenAI
from safety_client import build_openai_client, provider_name
from safety_models import build_redaction_result, extract_moderation_output, redact_text_from_categories

MODEL = "omni-moderation-latest"


def redact_unsafe(text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_openai_client()
    response = client.moderations.create(model=MODEL, input=text)
    parsed = extract_moderation_output(response)
    redacted_text, spans = redact_text_from_categories(text, parsed.get("categories", {}))
    return build_redaction_result(
        provider=provider_name(),
        operation="redact_unsafe",
        input_text=text,
        redacted_text=redacted_text,
        spans=spans,
        moderation=parsed,
        metadata=metadata,
    )
