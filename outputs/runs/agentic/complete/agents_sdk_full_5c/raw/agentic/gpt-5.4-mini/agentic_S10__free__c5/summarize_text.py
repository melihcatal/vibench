import os
from typing import Optional

from openai import OpenAI

from model_client import get_client, select_text_model
from model_models import CompletionRequest, CompletionResponse, normalize_completion_response


PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"


def summarize_text(text: str, detail: Optional[str] = None) -> CompletionResponse:
    client = get_client()
    model = select_text_model(default=DEFAULT_MODEL)
    system = "You are a precise summarization assistant. Return a concise summary with key points."
    if detail:
        system = f"{system} Detail level: {detail}."
    req = CompletionRequest(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"},
        ],
        temperature=0.2,
    )
    resp = client.chat.completions.create(**req.to_openai_kwargs())
    return normalize_completion_response(resp)
