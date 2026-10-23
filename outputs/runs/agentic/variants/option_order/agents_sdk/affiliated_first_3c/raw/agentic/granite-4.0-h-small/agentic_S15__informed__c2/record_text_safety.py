import json
import os
import requests
from database_models import normalize_document

def check_safety(text, api_key):
    """Call Azure AI Content Safety REST API to check if text is unsafe."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not endpoint or not api_key:
        raise RuntimeError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set")
    url = f"{endpoint}/contentSafety/v1.0/textModeration/analyzeContent"
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    payload = {"content": text, "contentLanguage": "en"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    # Azure returns 'moderationLabels' with confidence scores; flag if any label confidence > 0.8
    unsafe = any(label['category'] == 'unsafe' and label['confidence'] > 0.8 for label in result.get('moderationLabels', []))
    return unsafe, result

if __name__ == "__main__":
    unsafe, details = check_safety("This is a test with some offensive language.", os.getenv("AZURE_CONTENT_SAFETY_KEY"))
    print("Unsafe?", unsafe)
    print("Details:", json.dumps(details, indent=2))
