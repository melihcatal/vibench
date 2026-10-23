import os
from typing import Dict, Any
from openai import OpenAI
from model_client import get_openai_client
from model_models import ChatRequest, ChatResponse


def collect_platform_metadata(prompt: str, model_id: str = "gpt-4o") -> Dict[str, Any]:
    """
    Return model output together with OpenAI platform metadata.
    """
    client = get_openai_client()

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
        )

        # Extract metadata from OpenAI response
        metadata = {
            "provider": "openai",
            "model_id": response.model,
            "created_timestamp": response.created,
            "object_type": response.object,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
            "index": response.choices[0].index,
            "system_fingerprint": getattr(response, "system_fingerprint", None),
            "response_id": response.id,
        }

        # Create normalized response
        chat_response = ChatResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage=metadata["usage"],
            raw_response=response,
        )

        return {
            "content": chat_response.content,
            "metadata": metadata,
            "normalized_response": chat_response,
            "raw_openai_response": response,
        }

    except Exception as e:
        raise Exception(
            f"Failed to collect metadata from OpenAI model {model_id}: {str(e)}"
        )
