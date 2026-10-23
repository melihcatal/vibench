from __future__ import annotations

from openai import OpenAI

from model_client import choose_model, get_openai_client, normalize_messages
from model_models import LLMRequest, LLMResponse, coerce_text


def summarize_text(text: str, model: str | None = None) -> LLMResponse:
    client: OpenAI = get_openai_client()
    request = LLMRequest(
        prompt=text,
        system="Summarize the provided text concisely and accurately.",
        model=choose_model(model, family="chat"),
        temperature=0.2,
        max_tokens=256,
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=normalize_messages(request.system, request.prompt),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return LLMResponse(text=coerce_text(response.choices[0].message.content), model=request.model, raw=response)
