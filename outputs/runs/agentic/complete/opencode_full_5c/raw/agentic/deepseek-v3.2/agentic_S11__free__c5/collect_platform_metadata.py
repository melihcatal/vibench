import os
from typing import Dict, Any
from openai import OpenAI
from model_client import get_openai_client
from model_models import ChatResponse


def collect_platform_metadata(prompt: str, model: str = "gpt-4o") -> Dict[str, Any]:
    """Return model output together with provider platform metadata such as usage, resource IDs, or model handles."""
    client = get_openai_client()

    # Make API call to OpenAI
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
    )

    # Extract content
    content = response.choices[0].message.content

    # Collect comprehensive metadata from OpenAI response
    metadata = {
        "content": content,
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "response_id": response.id,
        "created": response.created,
        "object_type": response.object,
        "choices_count": len(response.choices),
        "finish_reason": response.choices[0].finish_reason,
        "provider": "openai",
        "api_version": "2024-11-01",  # OpenAI API version
        "model_family": "gpt-4"
        if "gpt-4" in model
        else "gpt-3.5"
        if "gpt-3.5" in model
        else "other",
    }

    # Add system metadata
    metadata["system"] = {
        "rate_limit_remaining": getattr(response, "_headers", {}).get(
            "x-ratelimit-remaining-requests", "unknown"
        ),
        "rate_limit_reset": getattr(response, "_headers", {}).get(
            "x-ratelimit-reset-requests", "unknown"
        ),
        "request_id": getattr(response, "_headers", {}).get("x-request-id", "unknown"),
    }

    return metadata


def get_model_info(model: str = "gpt-4o") -> Dict[str, Any]:
    """Get detailed information about a specific OpenAI model."""
    # This is a simplified version - in production you might call models.retrieve()
    model_info = {
        "gpt-4o": {
            "id": "gpt-4o",
            "object": "model",
            "created": 1687882411,
            "owned_by": "openai",
            "context_length": 128000,
            "capabilities": ["chat", "vision", "function_calling"],
            "max_tokens": 4096,
        },
        "gpt-4o-mini": {
            "id": "gpt-4o-mini",
            "object": "model",
            "created": 1687882412,
            "owned_by": "openai",
            "context_length": 128000,
            "capabilities": ["chat", "function_calling"],
            "max_tokens": 16384,
        },
    }

    return model_info.get(model, {})


if __name__ == "__main__":
    # Example usage
    metadata = collect_platform_metadata("What is the capital of France?")
    print("Response metadata:")
    for key, value in metadata.items():
        if key != "content":
            print(f"{key}: {value}")

    print(f"\nContent preview: {metadata['content'][:100]}...")

    model_info = get_model_info("gpt-4o")
    print(f"\nModel info: {model_info}")
