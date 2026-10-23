"""Check secret labels and notes for unsafe text using Azure AI Content Safety."""
import os
import requests
import json

def check_label_safety(text_to_check: str) -> dict:
    """
    Analyzes text for harmful content using the Azure AI Content Safety API.

    Args:
        text_to_check: The input text (e.g., a secret's description or label).

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety endpoint and key must be set in environment variables.")

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01"
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key
    }

    payload = {
        "text": text_to_check,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred calling Azure AI Content Safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage:
    # Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    
    safe_text = "This is the API key for the production database."
    unsafe_text = "I hate this terrible key, I want to attack the system."
    
    print("--- Checking safe text ---")
    safe_result = check_label_safety(safe_text)
    print(json.dumps(safe_result, indent=2))
    
    print("\n--- Checking unsafe text ---")
    unsafe_result = check_label_safety(unsafe_text)
    print(json.dumps(unsafe_result, indent=2))
