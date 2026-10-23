import os
import requests
import json
from typing import Dict, Any

def moderate_vendor_text(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    api_version = "2023-10-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }

    data = {
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
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Process results to determine safety
        is_safe = True
        for category in result.get("categoriesAnalysis", []):
            if category["severity"] > 0: # Severity > 0 indicates potential issue
                is_safe = False
                break
        
        return {"success": True, "is_safe": is_safe, "analysis": result}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
