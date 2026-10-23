from typing import Iterator, Dict, Any
from model_client import ModelClient
from model_models import StreamChunk
from azure.ai.inference.models import ChatCompletionsResponse


def stream_platform_generation(
    system_prompt: str, user_prompt: str
) -> Iterator[StreamChunk]:
    """Streams output from Azure AI Inference 'gpt-4o' model while preserving provider response objects."""
    client = ModelClient().get_client()

    messages = ModelClient().prepare_messages(
        system_prompt=system_prompt, user_prompt=user_prompt
    )

    response: Iterator[ChatCompletionsResponse] = client.complete_stream(
        messages=messages, model="gpt-4o", temperature=0.7, max_tokens=1000
    )

    for chunk in response:
        yield StreamChunk(
            id=chunk.id,
            content=chunk.choices[0].delta.content if chunk.choices[0].delta else "",
            finish_reason=chunk.choices[0].finish_reason,
            usage={
                "prompt_tokens": chunk.usage.prompt_tokens,
                "completion_tokens": chunk.usage.completion_tokens,
                "total_tokens": chunk.usage.total_tokens,
            }
            if chunk.usage
            else None,
        )
