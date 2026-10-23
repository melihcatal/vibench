import os
from typing import Optional
from model_client import get_vertex_ai_client
from model_models import VertexAIRequest, VertexAIResponse


def invoke_vertex_ai_model(
    prompt: str,
    model_id: str = "gemini-1.5-pro-001",
    temperature: float = 0.7,
    max_tokens: int = 1024,
    project: Optional[str] = None,
    location: Optional[str] = None,
) -> VertexAIResponse:
    """
    Invoke a Vertex AI managed model with the given prompt and parameters.
    
    Args:
        prompt: Input text prompt for the model.
        model_id: Vertex AI model identifier (e.g., "gemini-1.5-pro-001").
        temperature: Sampling temperature.
        max_tokens: Maximum number of tokens to generate.
        project: Google Cloud project ID. Defaults to environment variable.
        location: Google Cloud region. Defaults to environment variable.
    
    Returns:
        VertexAIResponse containing the model's text output and metadata.
    """
    client = get_vertex_ai_client()
    
    request = VertexAIRequest(
        prompt=prompt,
        model_id=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    
    response = client.generate_text(
        project=project or os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        model=request.model_id,
        prompt=request.prompt,
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
    )
    
    return VertexAIResponse.from_vertex_ai_response(response)