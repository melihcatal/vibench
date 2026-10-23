from __future__ import annotations

from safety_client import get_azure_openai_client, safety_model_name
from safety_models import RedactionRequest, RedactionResult, normalize_redaction_response


REDACTION_PROMPT = """Redact unsafe spans in the text.\nReturn JSON with keys: redacted_text, spans, categories.\nReplace unsafe spans with [REDACTED].\n"""


def redact_unsafe(text: str) -> RedactionResult:
    request = RedactionRequest(text=text)
    client = get_azure_openai_client()
    response = client.chat.completions.create(  # azure-openai SDK
        model=safety_model_name("redaction"),
        messages=[
            {"role": "system", "content": REDACTION_PROMPT},
            {"role": "user", "content": request.to_prompt()},
        ],
        temperature=0,
    )
    return normalize_redaction_response(response)
