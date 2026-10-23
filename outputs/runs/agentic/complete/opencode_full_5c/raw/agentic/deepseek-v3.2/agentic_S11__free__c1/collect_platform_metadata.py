import os
from typing import Dict, Any
from openai import OpenAI
from model_client import get_platform_client
from model_models import PlatformRequest, PlatformResponse


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    """Returns model output together with provider platform metadata such as usage, resource IDs, or model handles."""
    client = get_platform_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_message},
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False,
        )

        metadata = {
            "provider": "openai",
            "model_id": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "created": response.created,
            "id": response.id,
            "object": response.object,
            "choices_count": len(response.choices),
            "finish_reason": response.choices[0].finish_reason,
        }

        return PlatformResponse(
            content=response.choices[0].message.content,
            model_id=response.model,
            usage=response.usage,
            raw_response=response,
            metadata=metadata,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to collect OpenAI metadata: {str(e)}")
