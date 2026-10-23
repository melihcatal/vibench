"""Invoke a provider-managed model through an OpenAI inference client."""

import os

from openai import OpenAI

from model_client import get_openai_client, PLATFORM_MODEL_DEFAULT
from model_models import PlatformRequest, PlatformResponse


def invoke_platform_model(
    prompt: str,
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> PlatformResponse:
    """Invoke the OpenAI platform model identified by MODEL_ID.

    Uses the OPENAI_API_KEY environment variable and the OpenAI Python SDK
    client to send a chat-completion request to api.openai.com.
    """
    model_id = model or PLATFORM_MODEL_DEFAULT
    client = get_openai_client()

    request = PlatformRequest(
        prompt=prompt,
        model=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    response = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    raw_text = response.choices[0].message.content or ""
    finish_reason = response.choices[0].finish_reason

    return PlatformResponse(
        text=raw_text,
        finish_reason=finish_reason,
        model=model_id,
        raw_response=response,
    )


if __name__ == "__main__":
    result = invoke_platform_model("Explain quantum computing in two sentences.")
    print(result.text)
