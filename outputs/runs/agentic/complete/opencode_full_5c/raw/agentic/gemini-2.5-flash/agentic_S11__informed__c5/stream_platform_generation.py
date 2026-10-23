from model_client import VertexAIClient
from model_models import PlatformModelRequest, PlatformStreamResponse
from vertexai.preview.generative_models import GenerationConfig


def stream_platform_generation(request: PlatformModelRequest) -> PlatformStreamResponse:
    """Streams output from a managed model platform while preserving provider response objects."""
    client = VertexAIClient()
    model = client.get_model(request.model_id or "gemini-pro")  # Default to gemini-pro

    generation_config = GenerationConfig(
        temperature=request.parameters.get("temperature", 0.7),
        top_p=request.parameters.get("top_p", 0.95),
        top_k=request.parameters.get("top_k", 40),
        max_output_tokens=request.parameters.get("max_output_tokens", 1024),
    )

    response_stream = model.generate_content(
        request.prompt, generation_config=generation_config, stream=True
    )

    chunks = []
    metadata = {}
    for chunk in response_stream:
        chunks.append(chunk.text)
        # Example of collecting metadata from each chunk if available
        # For Vertex AI, usage_metadata is typically at the end of the stream.
        if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
            metadata["prompt_tokens"] = chunk.usage_metadata.prompt_token_count
            metadata["candidates_tokens"] = chunk.usage_metadata.candidates_token_count

    return PlatformStreamResponse(chunks=chunks, metadata=metadata)
