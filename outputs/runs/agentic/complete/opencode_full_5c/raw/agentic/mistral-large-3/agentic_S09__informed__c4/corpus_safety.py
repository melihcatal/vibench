from typing import List
import requests
import os


def check_corpus_safety(texts: List[str]) -> Dict[str, any]:
    """
    Checks corpus text for harmful content using Azure AI Content Safety.

    Args:
        texts: List of texts to check for safety.

    Returns:
        Dictionary containing safety analysis results for each text.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY not set."
        )

    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    results = []
    for text in texts:
        body = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "breakByBlock": False,
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        results.append(response.json())

    return {"results": results}
