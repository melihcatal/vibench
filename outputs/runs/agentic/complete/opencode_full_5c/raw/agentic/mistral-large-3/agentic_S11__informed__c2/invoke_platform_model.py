from typing import Optional, Dict, Any
import os
from huggingface_hub import InferenceClient
from model_client import get_model_client_config
from model_models import ModelRequest, ModelResponse


def invoke_platform_model(request: ModelRequest) -> ModelResponse:
    """
    Invokes a Hugging Face Inference Endpoint or Inference API model.
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

        return ModelResponse(
            output=response.generated_text,
            details={
                "tokens_generated": response.details.generated_tokens,
                "finish_reason": response.details.finish_reason,
                "model_id": request.model_id,
            },
        )
    except Exception as e:
        raise RuntimeError(f"Hugging Face Inference failed: {str(e)}")
