import os
import requests
from typing import Dict, Any


def check_corpus_safety(text: str) -> Dict[str, Any]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "blocklistNames": [],
        "breakIntoSentences": True,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "details": response.text if response else "No response",
        }


if __name__ == "__main__":
    os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = (
        "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"  # Placeholder
    )
    os.environ["AZURE_CONTENT_SAFETY_KEY"] = (
        "YOUR_AZURE_CONTENT_SAFETY_KEY"  # Placeholder
    )

    sample_text = "This is a benign test sentence. I hate bad people."
    safety_results = check_corpus_safety(sample_text)
    # print("Azure AI Content Safety Results:", safety_results)
