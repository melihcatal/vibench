import os
import requests
import json

def moderate_text(text: str) -> dict:
    # Azure AI Content Safety API configuration
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        print("Azure Content Safety endpoint and key are not set in environment variables.")
        return {"error": "Configuration missing"}

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error moderating text with Azure Content Safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY)
    # Set these environment variables before running.
    test_text_clean = "This is a normal conversation and poses no harm."
    test_text_harmful = "I will hurt you!"

    print("Moderating clean text:")
    result_clean = moderate_text(test_text_clean)
    print(json.dumps(result_clean, indent=2))

    print("\nModerating potentially harmful text:")
    result_harmful = moderate_text(test_text_harmful)
    print(json.dumps(result_harmful, indent=2))
