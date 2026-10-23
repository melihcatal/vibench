import os
import requests
import json

def check_text_for_safety(text: str, endpoint: str, key: str) -> dict:
    """Checks narration scripts for unsafe content using Azure AI Content Safety.

    Args:
        text: The text content to check.
        endpoint: The Azure AI Content Safety endpoint URL (e.g., "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com").
        key: The Azure AI Content Safety subscription key.

    Returns:
        A dictionary containing the moderation analysis results.
    """
    api_version = "2023-04-30-preview"
    path = "text:analyze?api-version=" + api_version
    url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }

    body = {
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
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking text for safety: {e}")
        return {"error": str(e)}


if __name__ == '__main__':
    # Replace with your Azure AI Content Safety endpoint and key
    # AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    # AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    # if AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY:
    #     safe_text = "This is a perfectly safe script for narration."
    #     print(f"\nChecking safe text: '{safe_text}'")
    #     result_safe = check_text_for_safety(safe_text, AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY)
    #     print(json.dumps(result_safe, indent=2))

    #     unsafe_text = "I hate you so much, I want to hurt you."
    #     print(f"\nChecking unsafe text: '{unsafe_text}'")
    #     result_unsafe = check_text_for_safety(unsafe_text, AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY)
    #     print(json.dumps(result_unsafe, indent=2))
    # else:
    #     print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
    
    print("\nSimulated content safety check. Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to run actual checks.")
    print(json.dumps({"categoriesAnalysis": []}, indent=2))
