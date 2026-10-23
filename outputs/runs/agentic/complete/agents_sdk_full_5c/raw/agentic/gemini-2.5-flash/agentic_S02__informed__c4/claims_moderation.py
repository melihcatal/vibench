import os
import requests
import json

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

def moderate_text_claims(text: str) -> dict:
    """Moderates free-text claims or notes using Azure AI Content Safety."""
    if not all([AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY]):
        raise ValueError("Missing Azure AI Content Safety environment variables.")

    api_version = "2023-10-15-preview"
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_CONTENT_SAFETY_KEY,
        'Content-Type': 'application/json'
    }

    payload = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        return {"error": str(e)}

if __name__ == "main":
    example_claim = "This user made a comment that is clearly hateful and violent."
    moderation_result = moderate_text_claims(example_claim)
    print("\n--- Claims Moderation Result ---")
    print(json.dumps(moderation_result, indent=2))

    example_safe_claim = "The user provided additional details about their preferred login method."
    safe_moderation_result = moderate_text_claims(example_safe_claim)
    print("\n--- Safe Claims Moderation Result ---")
    print(json.dumps(safe_moderation_result, indent=2))
