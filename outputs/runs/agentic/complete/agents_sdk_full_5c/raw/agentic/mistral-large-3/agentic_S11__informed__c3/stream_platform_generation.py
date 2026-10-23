import os
from typing import Iterator
from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import Prediction
from model_models import VertexAIStreamChunk


def stream_vertex_ai_generation(
    prompt: str,
    model_id: str = "gemini-1.5-pro-001",
    temperature: float = 0.7,
    max_tokens: int = 1024,
    project: Optional[str] = None,
    location: Optional[str] = None,
) -> Iterator[VertexAIStreamChunk]:
    """
    Stream text generation from a Vertex AI managed model.
    
    Args:
        prompt: Input text prompt for the model.
        model_id: Vertex AI model identifier (e.g., "gemini-1.5-pro-001").
        temperature: Sampling temperature.
        max_tokens: Maximum number of tokens to generate.
        project: Google Cloud project ID. Defaults to environment variable.
        location: Google Cloud region. Defaults to environment variable.
    
    Yields:
        VertexAIStreamChunk containing a chunk of text and metadata.
    """
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={
            "api_endpoint": f"{location or os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')}-aiplatform.googleapis.com"
        }
    )
    
    endpoint = f"projects/{project or os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/{location or os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')}/publishers/google/models/{model_id}"
    
    instance = {"prompt": prompt}
    parameters = {
        "temperature": temperature,
        "maxOutputTokens": max_tokens,
    }
    
    response_stream = client.stream_raw_predict(
        endpoint=endpoint, instances=[instance], parameters=parameters
    )
    
    for response in response_stream:
        chunk = VertexAIStreamChunk.from_vertex_ai_stream(response)
        yield chunk