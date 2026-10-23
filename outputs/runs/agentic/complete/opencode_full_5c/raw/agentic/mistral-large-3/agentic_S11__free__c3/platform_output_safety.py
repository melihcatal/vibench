from typing import Dict, Any
import requests
from .model_client import get_model_client_config
from .model_models import ChatResponse


def platform_output_safety(
    response: ChatResponse,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Checks Azure AI Content Safety for unsafe content in model output.
    """
    config = get_model_client_config()
    api_key = api_key or config.get("AZURE_CONTENT_SAFETY_KEY")
    endpoint = config.get("AZURE_CONTENT_SAFETY_ENDPOINT")

    if not all([api_key, endpoint]):
        raise ValueError("Missing required configuration for Azure Content Safety.")

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": response.content,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
    }

    safety_response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01",
        headers=headers,
        json=payload,
    )
    safety_response.raise_for_status()

    results = safety_response.json()
    is_safe = all(
        result["severity"] < 2 for result in results.get("categoriesAnalysis", [])
    )

    return {
        "is_safe": is_safe,
        "safety_results": results,
    }
