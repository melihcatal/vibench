import os
import requests
from safety_client import get_content_safety_client
from safety_models import TextModerationResult

def redact_unsafe(text: str, redaction_placeholder: str = "[REDACTED UNSAFE CONTENT]") -> str:
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    
    Note: Azure AI Content Safety's 'text:analyze' API primarily provides category severities.
    For direct span redaction, you would typically use its blocklist feature or combine with
    other NLP services for identifying specific unsafe spans. This implementation
    redacts the entire text if any category is detected as unsafe (severity > 0).
    """
    client = get_content_safety_client()
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        is_unsafe = False
        if "categoriesAnalysis" in result:
            for category_analysis in result["categoriesAnalysis"]:
                if category_analysis["severity"] > 0: 
                    is_unsafe = True
                    break
        
        if is_unsafe:
            return redaction_placeholder
        else:
            return text

    except requests.exceptions.RequestException as e:
        print(f"Error redacting text with Azure AI Content Safety: {e}")
        # In case of an error, it's safer to redact
        return redaction_placeholder
