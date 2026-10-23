import os
from typing import Iterator

from mistralai import Mistral
from mistralai.models import ChatCompletionResponse, ChatCompletionChunk

from model_models import (
    LLMRequest,
    LLMResponse,
    StreamChunk,
    ChatMessage,
)

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")
MISTRAL_DEFAULT_MODEL = "mistral-large-latest"
MISTRAL_EMBED_MODEL = "mistral-embed"


def get_mistral_client() -> Mistral:
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    return Mistral(api_key=MISTRAL_API_KEY)


def to_mistral_messages(messages: list[ChatMessage]) -> list[dict]:
    return [{"role": m.role, "content": m.content} for m in messages]


def execute_chat(request: LLMRequest) -> LLMResponse:
    client = get_mistral_client()
    mistral_messages = to_mistral_messages(request.messages)

    kwargs: dict = {
        "model": request.model or MISTRAL_DEFAULT_MODEL,
        "messages": mistral_messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
    }
    if request.response_format:
        kwargs["response_format"] = request.response_format

    response: ChatCompletionResponse = client.chat.complete(**kwargs)

    content = ""
    if response.choices and response.choices[0].message:
        content = response.choices[0].message.content or ""

    usage = response.usage
    return LLMResponse(
        content=content,
        model=response.model,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        finish_reason=response.choices[0].finish_reason if response.choices else "",
    )


def execute_stream_chat(request: LLMRequest) -> Iterator[StreamChunk]:
    client = get_mistral_client()
    mistral_messages = to_mistral_messages(request.messages)

    kwargs: dict = {
        "model": request.model or MISTRAL_DEFAULT_MODEL,
        "messages": mistral_messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
    }

    stream = client.chat.stream(**kwargs)
    for chunk in stream:
        data: ChatCompletionChunk = chunk.data
        if data.choices and data.choices[0].delta:
            delta_content = data.choices[0].delta.content or ""
            finish = data.choices[0].finish_reason
            yield StreamChunk(
                delta=delta_content,
                model=data.model,
                finish_reason=finish,
            )
