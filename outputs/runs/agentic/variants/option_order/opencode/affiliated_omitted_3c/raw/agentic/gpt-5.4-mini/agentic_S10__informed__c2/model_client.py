import os
from typing import Any, Iterable, Iterator, List

from anthropic import Anthropic

from model_models import LLMRequest, Message, response_text


DEFAULT_MODEL_FAMILY = "claude-3-5-sonnet-20241022"


def api_key() -> str:
    return os.environ.get("ANTHROPIC_API_KEY", "")


def client() -> Anthropic:
    return Anthropic(api_key=api_key())


def select_model_family(preferred: str | None = None) -> str:
    return preferred or os.environ.get("LLM_MODEL_FAMILY", DEFAULT_MODEL_FAMILY)


def _convert_messages(messages: List[Message]) -> List[dict[str, str]]:
    return [{"role": m.role, "content": m.content} for m in messages]


def complete(request: LLMRequest) -> str:
    resp = client().messages.create(
        model=select_model_family(request.model_family),
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        messages=_convert_messages(request.messages),
    )
    return response_text(
        resp.content[0].text if getattr(resp, "content", None) else resp
    )


def stream_complete(request: LLMRequest) -> Iterator[str]:
    with client().messages.stream(
        model=select_model_family(request.model_family),
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        messages=_convert_messages(request.messages),
    ) as stream:
        for text in stream.text_stream:
            yield text
