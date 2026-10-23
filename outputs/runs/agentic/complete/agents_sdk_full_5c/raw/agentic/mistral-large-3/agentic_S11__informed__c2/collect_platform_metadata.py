from typing import Dict, Any
from model_client import get_vertex_ai_client
from model_models import ModelRequest, ModelResponseWithMetadata


def collect_model_metadata(
    request: ModelRequest,
    model_id: str = "gemini-1.5-pro-001",
) -> ModelResponseWithMetadata:
    """Invoke a Vertex AI model and collect platform metadata."""
    client = get_vertex_ai_client()
    
    model = client.get_generative_model(model_name=model_id)
    response = model.generate_content(request.prompt)
    
    metadata: Dict[str, Any] = {
        "model_id": model_id,
        "resource_name": model._model_name,
        "usage": {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count,
        },
        "safety_ratings": [{
            "category": rating.category,
            "probability": rating.probability,
        } for rating in response.candidates[0].safety_ratings],
    }
    
    return ModelResponseWithMetadata(
        output=response.text,
        metadata=metadata,
    )