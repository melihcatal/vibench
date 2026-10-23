from typing import Any, Dict

from openai import OpenAI

from safety_client import get_openai_client, moderation_model_name
from safety_models import normalize_redaction_result


def redact_unsafe(text: str) -> Dict[str, Any]:
    client = get_openai_client()
    model = moderation_model_name()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Identify unsafe spans in the text and return JSON with redacted_text, spans, and category labels. Keep safe content intact.",
            },
            {"role": "user", "content": text},
        ],
        text={"format": {"type": "json_object"}},
    )
    return normalize_redaction_result(response.output_text)
