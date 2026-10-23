# payload_safety.py
import os
import requests
import json

def check_payload_safety_azure(text_content: str) -> dict:
    """
    Checks decrypted text content for safety using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set.")

    url = f"{endpoint}contentsafety/text:analyze?api-version=2023-10-01"
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    payload = {
        "text": text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    
    analysis = response.json()
    
    is_safe = all(cat['severity'] == 0 for cat in analysis['categoriesAnalysis'])
    
    return {
        "is_safe": is_safe,
        "analysis": analysis
    }
