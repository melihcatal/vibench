from google import genai
from model_models import ModelInvocationPayload, ModelConfig
from model_client import get_vertex_ai_client
from typing import Iterator, Dict, Any

def stream_platform_generation(
    payload: ModelInvocationPayload, config: ModelConfig
) -> Iterator[Dict[str, Any]]:
    client = get_vertex_ai_client(config.project_id, config.location)
    model = client.get_model(config.model_id)

    # Use the generate_content method with stream=True for streaming responses
    response_stream = model.generate_content(
        payload.text, stream=True
    )

    for chunk in response_stream:
        yield {
            "text_chunk": chunk.text,
            "finish_reason": chunk.finish_reason.name if chunk.finish_reason else None,
            "metadata": {"prompt_token_count": chunk.usage_metadata.prompt_token_count if chunk.usage_metadata else 0, # Placeholder, actual streaming metadata may vary
                         "candidates_token_count": chunk.usage_metadata.candidates_token_count if chunk.usage_metadata else 0}
        }
