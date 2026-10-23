from typing import Dict, Any

def normalize_model_response(response: Any) -> Dict[str, Any]:
    """Normalizes the model response into a consistent dictionary format."""
    # This is a placeholder. Real normalization would depend on the response object structure.
    if hasattr(response, 'text'):
        return {"text": response.text}
    return {"raw_response": str(response)}

def get_model_family(model_id: str) -> str:
    """Determines the model family from the model ID."""
    if "gemini" in model_id:
        return "gemini"
    return "unknown"
