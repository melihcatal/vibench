from typing import Generator, Optional

from dashscope import Generation

from model_client import (
    configure_dashscope_client,
    build_platform_request,
    DEFAULT_CHAT_MODEL,
)
from model_models import PlatformStreamChunk
from select_platform_resource import resolve_dashscope_model


def stream_platform_generation(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
) -> Generator[PlatformStreamChunk, None, None]:
    configure_dashscope_client()

    resolved = resolve_dashscope_model(model_hint=model, capability="chat")
    actual_model = resolved.model_id

    request = build_platform_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=actual_model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
    )

    payload = request.to_dashscope_payload()
    stream_response = Generation.call(**payload)

    for chunk in stream_response:
        if hasattr(chunk, "status_code") and chunk.status_code != 200:
            raise RuntimeError(
                f"DashScope / Alibaba Model Studio streaming error: "
                f"code={chunk.code}, message={chunk.message}"
            )
        yield PlatformStreamChunk.from_dashscope(chunk)


def collect_streamed_text(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
) -> str:
    full_text = ""
    for chunk in stream_platform_generation(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
    ):
        full_text += chunk.text_delta
    return full_text
