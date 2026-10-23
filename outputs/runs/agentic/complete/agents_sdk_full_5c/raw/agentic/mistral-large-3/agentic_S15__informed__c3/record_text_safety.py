from typing import Dict, Any
import requests
import os

def check_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def check_document_safety(document: Dict[str, Any], fields: list[str]) -> Dict[str, Any]:
    results = {}
    for field in fields:
        text = str(document.get(field, ""))
        results[field] = check_text_safety(text)
    return results