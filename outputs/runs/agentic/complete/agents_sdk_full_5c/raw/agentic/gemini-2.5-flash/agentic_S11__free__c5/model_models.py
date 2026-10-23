from typing import List, Dict, Any

class ModelRequest:
    """Defines a generic model request."""
    def __init__(self, prompt: str, parameters: Dict[str, Any] = None):
        self.prompt = prompt
        self.parameters = parameters if parameters is not None else {}

class ModelResponse:
    """Defines a generic model response."""
    def __init__(self, text: str, metadata: Dict[str, Any] = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}

def normalize_vertex_ai_response(vertex_response) -> ModelResponse:
    """Normalizes a Google Cloud Vertex AI response into a generic ModelResponse."""
    text = vertex_response.text
    metadata = {
        "finish_reason": vertex_response.candidates[0].finish_reason.name if vertex_response.candidates else None,
        "safety_ratings": []
    }
    if vertex_response.candidates:
        for rating in vertex_response.candidates[0].safety_ratings:
            metadata["safety_ratings"].append({
                "category": rating.category.name,
                "probability": rating.probability.name
            })
    return ModelResponse(text=text, metadata=metadata)
