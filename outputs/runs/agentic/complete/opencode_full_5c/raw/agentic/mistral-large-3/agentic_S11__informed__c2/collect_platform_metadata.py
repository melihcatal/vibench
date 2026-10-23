from typing import Dict, Any, Tuple
import os
from huggingface_hub import InferenceClient
from model_client import get_model_client_config
from model_models import ModelRequest, ModelResponseWithMetadata


def collect_platform_metadata(request: ModelRequest) -> ModelResponseWithMetadata:
    """
    Invokes a Hugging Face Inference API or Endpoint model and collects metadata.
    """
    config = get_model_client_config()
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        raise ValueError("HF_TOKEN environment variable not set")

    client = InferenceClient(model=request.model_id, token=api_token)

    try:
        response = client.text_generation(
            prompt=request.prompt,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            stop_sequences=request.stop_sequences,
            details=True,
        )

        metadata = {
            "provider": "huggingface",
            "model_id": request.model_id,
            "usage": {
                "input_tokens": response.details.prefill_tokens,
                "output_tokens": response.details.generated_tokens,
                "total_tokens": response.details.prefill_tokens
                + response.details.generated_tokens,
            },
            "finish_reason": response.details.finish_reason,
            "warnings": response.details.warnings or [],
        }

        return ModelResponseWithMetadata(
            output=response.generated_text, metadata=metadata
        )
    except Exception as e:
        raise RuntimeError(f"Hugging Face metadata collection failed: {str(e)}")
