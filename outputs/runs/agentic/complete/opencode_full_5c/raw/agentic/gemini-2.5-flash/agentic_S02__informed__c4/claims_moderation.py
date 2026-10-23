import os
import requests
import json

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def moderate_text_claim(text_claim: str) -> dict:
    """
    Moderates a free-text claim using Azure AI Content Safety.
    Args:
        text_claim: The free-text string to moderate.
    Returns:
        A dictionary containing the moderation results from Azure AI Content Safety.
    """
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        return {"error": "Azure Content Safety endpoint or key not set."}

    api_version = "2023-10-01"
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={api_version}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {"text": text_claim}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error moderating text with Azure AI Content Safety: {e}"}


if __name__ == "__main__":
    sample_claim = "This is a user-provided note with some potentially offensive language like crap."
    moderation_result = moderate_text_claim(sample_claim)
    print("Moderation Result:")
    print(json.dumps(moderation_result, indent=2))
