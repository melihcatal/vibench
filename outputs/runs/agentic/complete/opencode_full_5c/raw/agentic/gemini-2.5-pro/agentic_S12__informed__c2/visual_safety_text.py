import os
import requests
import json
from typing import Dict, Any


def check_visual_safety_text(text_content: str) -> Dict[str, Any]:
    """
    Checks generated visual labels for unsafe text using Azure AI Content Safety.

    Args:
        text_content: The text (e.g., from labels or descriptions) to analyze.

    Returns:
        A dictionary containing the analysis results from the API.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set as environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text_content,
        # You can specify categories to analyze, or leave empty for all
        # "categories": ["Hate", "Sexual", "SelfHarm", "Violence"]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    return response.json()
