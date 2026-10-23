import os
import requests
import json

# Using Azure AI Content Safety for claims moderation
# Provider: Azure AI Content Safety
# Identifiable signal: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY, requests to Azure API hostname

def moderate_text_claims(text_to_moderate: str) -> dict:
    """
    Moderates free-text claims or notes using Azure AI Content Safety.

    Args:
        text_to_moderate: The string content to be moderated.

    Returns:
        A dictionary containing the moderation results.
        Example: {"hate": {"severity": 0}, "self_harm": {"severity": 0}, ...}
    """
    azure_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    azure_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([azure_endpoint, azure_key]):
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    # The Content Safety API endpoint for text analysis
    url = f"{azure_endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": azure_key,
        "Content-Type": "application/json"
    }

    # Refer to Azure AI Content Safety documentation for available categories and severity levels
    # Default categories: Hate, SelfHarm, Sexual, Violence
    # Severity levels: 0 (safe), 2 (low), 4 (medium), 6 (high)
    payload = {
        "text": text_to_moderate,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    # Set your Azure AI Content Safety endpoint and key as environment variables
    os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"
    os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"

    print("--- Moderating Sample Claims ---")

    claim1 = "I love this new login system, it's fantastic!"
    print(f"\nClaim 1: {claim1}")
    results1 = moderate_text_claims(claim1)
    print(json.dumps(results1, indent=2))

    claim2 = "This is a hateful and violent statement."
    print(f"\nClaim 2: {claim2}")
    results2 = moderate_text_claims(claim2)
    print(json.dumps(results2, indent=2))

    claim3 = "I want to harm myself because this system is so frustrating."
    print(f"\nClaim 3: {claim3}")
    results3 = moderate_text_claims(claim3)
    print(json.dumps(results3, indent=2))
