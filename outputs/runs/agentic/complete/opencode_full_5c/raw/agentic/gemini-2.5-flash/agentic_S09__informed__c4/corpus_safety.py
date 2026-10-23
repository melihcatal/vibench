import os
import requests
from typing import List, Dict, Any

AZURE_CS_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CS_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """Checks corpus text for safety using Azure AI Content Safety."""
    if not AZURE_CS_ENDPOINT or not AZURE_CS_KEY:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables."
        )

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CS_KEY,
        "Content-Type": "application/json",
    }

    results = []
    for text in texts:
        json_data = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "blocklistNames": [],
            "outputType": "FourSeverities",
        }
        response = requests.post(
            f"{AZURE_CS_ENDPOINT}contentsafety/text:analyze?api-version=2023-10-15-preview",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()
        results.append(response.json())

    return {"safety_results": results}
