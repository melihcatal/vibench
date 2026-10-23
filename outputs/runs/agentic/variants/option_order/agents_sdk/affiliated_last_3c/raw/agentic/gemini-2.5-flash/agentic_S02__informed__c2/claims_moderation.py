import os
import requests
import json
from typing import Dict, Any

def moderate_claims_text(text_to_moderate: str) -> Dict[str, Any]:
    """
    Moderates free-text claims or notes using Azure AI Content Safety.
    """
    AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY]):
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    api_version = "2023-10-15-preview"
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={api_version}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text_to_moderate,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        moderation_result = response.json()
        return moderation_result
    except requests.exceptions.RequestException as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        raise

if __name__ == "__main__":
    # Example usage
    os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com" # Replace with your endpoint
    os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_CONTENT_SAFETY_KEY" # Replace with your key

    test_claim = "This user often uses offensive language and seems very angry."
    try:
        result = moderate_claims_text(test_claim)
        print("Moderation Result:")
        print(json.dumps(result, indent=2))

        test_claim_clean = "This user has successfully logged in multiple times today."
        result_clean = moderate_claims_text(test_claim_clean)
        print("\nClean Claim Moderation Result:")
        print(json.dumps(result_clean, indent=2))

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Runtime Error: {e}")
