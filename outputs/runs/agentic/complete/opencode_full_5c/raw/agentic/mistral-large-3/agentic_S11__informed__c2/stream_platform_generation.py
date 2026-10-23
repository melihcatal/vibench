from typing import Iterator, Dict, Any
import os
from huggingface_hub import InferenceClient
from model_client import get_model_client_config
from model_models import StreamChunk


def stream_platform_generation(
    model_id: str,
    prompt: str,
    max_tokens: int = 100,
    temperature: float = 0.7,
    stop_sequences: Optional[list] = None,
) -> Iterator[StreamChunk]:
    """
    Streams text generation from a Hugging Face Inference API or Endpoint model.
    """
    config = get_model_client_config()
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        raise ValueError("HF_TOKEN environment variable not set")

    client = InferenceClient(model=model_id, token=api_token)

    try:
        for chunk in client.text_generation(
            prompt=prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            stop_sequences=stop_sequences,
            stream=True,
        ):
            yield StreamChunk(
                text=chunk.token.text,
                details={
                    "token_id": chunk.token.id,
                    "token_logprob": chunk.token.logprob,
                    "provider": "huggingface",
                },
            )
    except Exception as e:
        raise RuntimeError(f"Hugging Face streaming failed: {str(e)}")
