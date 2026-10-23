from typing import List

from openai import OpenAI

from safety_client import get_client, load_config
from safety_models import RedactionResult, normalize_text


def redact_unsafe(text: str) -> RedactionResult:
    cfg = load_config()
    client: OpenAI = get_client(cfg)
    normalized = normalize_text(text)
    response = client.responses.create(
        model=cfg.text_model,
        input=(
            "Identify unsafe spans in the following text and return JSON with keys 'redacted_text' "
            "and 'spans' using the exact text values to redact: " + normalized
        ),
    )
    output_text = response.output_text if hasattr(response, "output_text") else ""
    redacted_text = output_text or normalized
    return RedactionResult(text=redacted_text, redacted_spans=[])
