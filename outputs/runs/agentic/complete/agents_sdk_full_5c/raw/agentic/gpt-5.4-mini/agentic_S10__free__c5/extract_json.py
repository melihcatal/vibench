from openai import OpenAI

from model_client import get_client, select_structured_model
from model_models import CompletionRequest, CompletionResponse, normalize_completion_response


PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"


def extract_json(text: str, schema_hint: str) -> CompletionResponse:
    client = get_client()
    model = select_structured_model(default=DEFAULT_MODEL)
    req = CompletionRequest(
        model=model,
        messages=[
            {"role": "system", "content": "Extract structured JSON only. Do not include prose."},
            {"role": "user", "content": f"Text:\n{text}\n\nSchema hint:\n{schema_hint}"},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    resp = client.chat.completions.create(**req.to_openai_kwargs())
    return normalize_completion_response(resp)
