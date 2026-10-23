import os
import requests  # Tisane Text Moderation
from typing import Dict, Any


def check_annotation_safety(text: str) -> Dict[str, Any]:
    """Checks free-text metric labels or annotations for unsafe text using Tisane Text Moderation API.

    Args:
        text (str): The free-text annotation or label to check.

    Returns:
        Dict[str, Any]: A dictionary containing the moderation results from Tisane.
                        Example: {'has_unsafe_content': True, 'details': [...]}
    """
    tisane_api_key = os.environ.get("TISANE_API_KEY")
    if not tisane_api_key:
        raise ValueError("TISANE_API_KEY environment variable not set.")

    tisane_endpoint = "https://api.tisane.ai/beta/document"

    headers = {
        "Content-Type": "application/json",
        "X-TISANE-API-KEY": tisane_api_key,  # Provider-identifying signal: X-TISANE-API-KEY
    }

    payload = {
        "language": "en",  # Assuming English for annotations; could be configurable
        "text": text,
        "settings": {"with_latest_dictionaries": True, "detect_violations": True},
    }

    try:
        response = requests.post(tisane_endpoint, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Simple check for unsafe content based on Tisane's common response structure
        has_unsafe_content = False
        if result.get("annotations"):
            for annotation in result["annotations"]:
                if annotation.get("violations"):
                    has_unsafe_content = True
                    break

        return {
            "has_unsafe_content": has_unsafe_content,
            "details": result.get("annotations", []),
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Error checking text safety with Tisane: {e}"}
