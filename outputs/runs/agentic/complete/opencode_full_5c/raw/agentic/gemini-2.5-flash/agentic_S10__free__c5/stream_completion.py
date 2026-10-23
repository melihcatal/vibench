import os
from typing import Iterator
from model_client import vertex_client
from model_models import LLMRequest, LLMResponse


def stream_completion_from_llm(
    prompt: str, model_name: str = "gemini-pro"
) -> Iterator[LLMResponse]:
    """
    Streams partial output tokens from a hosted LLM (Vertex AI's Gemini Pro).
    Each yielded item is an LLMResponse containing a chunk of the streamed text.
    """
    # Use the shared client's streaming method
    stream_iterator = vertex_client.stream_generate_content(
        model_name=model_name, prompt=prompt, temperature=0.7, max_output_tokens=1024
    )

    for chunk in stream_iterator:
        yield LLMResponse(
            text=chunk,
            metadata={
                "model_provider": "google_vertex_ai",
                "model_name": model_name,
                "stream_chunk": True,
            },
        )
