from openai import OpenAI

from model_client import get_client, select_translation_model
from model_models import CompletionRequest, CompletionResponse, normalize_completion_response


PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"


def result_translate(text: str, target_language: str) -> CompletionResponse:
    client = get_client()
    model = select_translation_model(default=DEFAULT_MODEL)
    req = CompletionRequest(
        model=model,
        messages=[
            {"role": "system", "content": "Translate accurately while preserving meaning and formatting."},
            {"role": "user", "content": f"Translate to {target_language}:\n\n{text}"},
        ],
        temperature=0,
    )
    resp = client.chat.completions.create(**req.to_openai_kwargs())
    return normalize_completion_response(resp)
