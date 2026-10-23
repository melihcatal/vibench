from typing import Dict, Any
import os
import requests


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()

    return {
        "is_safe": all(block["severity"] == 0 for block in result.get("blocklistsMatch", []))
        and all(category["severity"] == 0 for category in result.get("categoriesAnalysis", [])),
        "categories_violated": [
            category["category"] for category in result.get("categoriesAnalysis", [])
            if category["severity"] > 0
        ]
    }