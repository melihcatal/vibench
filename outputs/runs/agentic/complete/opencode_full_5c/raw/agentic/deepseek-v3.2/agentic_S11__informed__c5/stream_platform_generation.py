import os
from typing import Generator
from openai import AzureOpenAI
from model_client import get_azure_client
from model_models import ChatRequest, StreamingChatResponse


def stream_platform_generation(
    request: ChatRequest,
) -> Generator[StreamingChatResponse, None, None]:
    """
    Stream output from Azure OpenAI while preserving provider response objects.
    """
    client = get_azure_client()

    try:
        stream = client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
        )

        full_content = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_content += content

                yield StreamingChatResponse(
                    content=content,
                    model=chunk.model,
                    finish_reason=chunk.choices[0].finish_reason
                    if chunk.choices[0].finish_reason
                    else None,
                    raw_chunk=chunk,
                )

    except Exception as e:
        raise RuntimeError(f"Failed to stream from Azure OpenAI: {e}")
