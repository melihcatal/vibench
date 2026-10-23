import os
from typing import Dict, Any, Optional
import requests


def check_prompt_safety(
    text: str,
    threshold: float = 0.5
) -> Optional[Dict[str, Any]]:
    """
    Check prompts and generated text for unsafe content using Azure AI Content Safety.
    
    Args:
        text: Text to check for unsafe content.
        threshold: Confidence threshold for flagging content.
        
    Returns:
        Dictionary containing safety analysis results or None if failed.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        return None

    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        for category in result.get("categoriesAnalysis", []):
            if category.get("severity", 0) >= threshold * 4:
                return {
                    "is_safe": False,
                    "category": category.get("category"),
                    "severity": category.get("severity")
                }
        return {"is_safe": True}
    return None