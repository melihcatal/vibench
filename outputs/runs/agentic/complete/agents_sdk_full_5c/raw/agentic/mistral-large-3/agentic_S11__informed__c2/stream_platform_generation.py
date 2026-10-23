import os
from typing import Iterator
from model_client import get_vertex_ai_client
from model_models import StreamChunk, ModelRequest


def stream_model_generation(
    request: ModelRequest,
    model_id: str = "gemini-1.5-pro-001",
    temperature: float = 0.7,
) -> Iterator[StreamChunk]:
    """Stream output from a Vertex AI managed model."""
    client = get_vertex_ai_client()
    
    generation_config = {
        "temperature": temperature,
        "max_output_tokens": request.max_tokens,
    }
    
    model = client.get_generative_model(model_name=model_id, generation_config=generation_config)
    response = model.generate_content(request.prompt, stream=True)
    
    for chunk in response:
        yield StreamChunk(
            text=chunk.text,
            metadata={
                "chunk_index": chunk._chunk_index,
                "model_id": model_id,
            }
        )