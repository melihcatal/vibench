import os
from typing import Dict, Any
from openai import OpenAI


def collect_platform_metadata(prompt: str, model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Returns model output together with provider platform metadata such as usage,
    resource IDs, or model handles from OpenAI's API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )

    # Extract metadata from OpenAI response
    metadata = {
        "content": response.choices[0].message.content,
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "finish_reason": response.choices[0].finish_reason,
        "response_id": response.id,
        "created_timestamp": response.created,
        "object_type": response.object,
    }

    return metadata
