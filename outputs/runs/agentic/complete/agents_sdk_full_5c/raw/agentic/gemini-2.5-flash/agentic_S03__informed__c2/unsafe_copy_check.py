import os
import requests
from typing import Dict, Any

def check_unsafe_content(text: str) -> Dict[str, Any]:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set)
    unsafe_text = "I will kill you."
    safe_text = "This is a safe sentence."

    print(f"Checking unsafe text: {unsafe_text}")
    result_unsafe = check_unsafe_content(unsafe_text)
    print(result_unsafe)

    print(f"\nChecking safe text: {safe_text}")
    result_safe = check_unsafe_content(safe_text)
    print(result_safe)
