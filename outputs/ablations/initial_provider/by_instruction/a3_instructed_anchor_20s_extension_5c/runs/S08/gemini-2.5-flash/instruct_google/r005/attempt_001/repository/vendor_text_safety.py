import os
from typing import Dict, Optional
import requests

def moderate_text_with_perspective_api(
    text: str,
    api_key: Optional[str] = None,
    threshold: float = 0.7,
) -> Dict[str, Union[bool, float]]:
    """Moderates text using Google Perspective API for potential toxicity."""

    api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Perspective API Key must be provided or set as environment variable PERSPECTIVE_API_KEY.")

    # https://developers.perspectiveapi.com/s/about-the-api
    # https://developers.perspectiveapi.com/s/docs-sample-requests
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"]
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        toxicity_score = result\
            .get("attributeScores", {})\
            .get("TOXICITY", {})\
            .get("summaryScore", {})\
            .get("value", 0.0)

        is_safe = toxicity_score < threshold

        return {"is_safe": is_safe, "toxicity_score": toxicity_score}

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"is_safe": False, "toxicity_score": 1.0, "error": str(e)}

def moderate_vendor_notes(
    vendor_note: str,
    api_key: Optional[str] = None,
    threshold: float = 0.7,
) -> Dict[str, Union[bool, float]]:
    """Moderates vendor notes or memo fields using Google Perspective API."""
    return moderate_text_with_perspective_api(vendor_note, api_key, threshold)
