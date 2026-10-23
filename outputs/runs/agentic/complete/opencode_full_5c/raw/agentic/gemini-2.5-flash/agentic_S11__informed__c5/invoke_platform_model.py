from model_client import VertexAIClient
from model_models import PlatformModelRequest, PlatformModelResponse
from vertexai.preview.generative_models import GenerationConfig


def invoke_platform_model(request: PlatformModelRequest) -> PlatformModelResponse:
    """Invokes a provider-managed model through a platform client."""
    client = VertexAIClient()
    model = client.get_model(request.model_id or "gemini-pro")  # Default to gemini-pro

    generation_config = GenerationConfig(
        temperature=request.parameters.get("temperature", 0.7),
        top_p=request.parameters.get("top_p", 0.95),
        top_k=request.parameters.get("top_k", 40),
        max_output_tokens=request.parameters.get("max_output_tokens", 1024),
    )

    response = model.generate_content(
        request.prompt, generation_config=generation_config
    )

    # Vertex AI specific metadata could be extracted from response.raw_content if available
    metadata = {
        "model_name": model.model_name,
        "prompt_tokens": response.usage_metadata.prompt_token_count
        if response.usage_metadata
        else None,
        "candidates_tokens": response.usage_metadata.candidates_token_count
        if response.usage_metadata
        else None,
    }

    return PlatformModelResponse(text=response.text, metadata=metadata)
