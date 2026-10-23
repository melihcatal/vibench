import os
import requests
import json
from typing import Dict, Any

def check_for_unsafe_content(text: str) -> Dict[str, Any]:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary summarizing the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    
    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    url = f"{endpoint}contentsafety/text:analyze?api-version=2023-10-01"
    
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    
    analysis = response.json()
    
    results = {
        "categories_analysis": [
            {"category": res["category"], "severity": res["severity"]}
            for res in analysis.get("categoriesAnalysis", [])
        ]
    }
    return results
