import os
import requests
from typing import Dict, Any
from identity_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY

def moderate_text_claims(text: str) -> Dict[str, Any]:
    """
    Moderates free-text claims or notes using Azure AI Content Safety.
    
    Args:
        text: The free text string to moderate.
        
    Returns:
        A dictionary containing moderation results.
    """
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        return {"error": "Azure Content Safety endpoint or key not configured."}

    api_version = "2023-10-01"
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={api_version}"
    
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json"
    }
    
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [] # Optionally include blocklists
    }
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Azure Content Safety API request failed: {e}", "details": str(e)}

if __name__ == "__main__":
    example_claim_note_safe = "User provided a helpful note about their login preferences."
    example_claim_note_unsafe = "This user is trying to spread hate speech and violence."
    
    print("Moderating safe text:")
    result_safe = moderate_text_claims(example_claim_note_safe)
    print(result_safe)
    
    print("\nModerating unsafe text:")
    result_unsafe = moderate_text_claims(example_claim_note_unsafe)
    print(result_unsafe)
