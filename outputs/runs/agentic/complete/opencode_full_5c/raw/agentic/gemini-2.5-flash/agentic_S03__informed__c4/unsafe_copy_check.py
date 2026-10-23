import os
import requests  # Provider-specific for REST API
from typing import List, Dict, Any


def check_unsafe_content(texts: List[str], language_code: str = "en") -> Dict[str, Any]:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety API.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    results = {}
    for i, text in enumerate(texts):
        data = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            analysis_result = response.json()
            results[f"Text_{i + 1}"] = analysis_result
        except requests.exceptions.RequestException as e:
            results[f"Text_{i + 1}"] = {
                "error": str(e),
                "message": "Failed to analyze content.",
            }
    return results
