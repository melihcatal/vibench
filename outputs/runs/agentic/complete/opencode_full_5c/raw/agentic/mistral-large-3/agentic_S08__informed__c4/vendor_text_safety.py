from typing import Dict, Any
import os
import requests


def vendor_text_safety(text: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "haltOnBlocklistHit": False,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    is_safe = all(
        result["categoriesAnalysis"][i]["severity"] < 2
        for i in range(len(result["categoriesAnalysis"]))
    )

    return {
        "is_safe": is_safe,
        "categories": result["categoriesAnalysis"],
        "blocklists": result.get("blocklistsMatch", []),
    }
