import os
import requests
from model_models import format_chat_response

def check_safety(text: str, provider: str = "perspective") -> Dict[str, Any]:
    """Check prompt or generated text for unsafe content using a hosted safety service.

    Args:
        text (str): Text to evaluate.
        provider (str): Safety service identifier (default 'perspective').
    Returns:
        dict: Assessment result.
    """
    if provider == "perspective":
        # Perspective API endpoint & key (hosted safety service)
        endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        api_key = os.getenv("PERSPECTIVE_API_KEY")
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
        }
        headers = {"Content-Type": "application/json", "x-api-key": api_key}
        resp = requests.post(endpoint, json=payload, headers=headers)
        resp.raise_for_status()
        result = resp.json()
        return result
    else:
        # Fallback placeholder safety check (no actual provider)
        return {"safe": True, "details": "No safety check performed"}
