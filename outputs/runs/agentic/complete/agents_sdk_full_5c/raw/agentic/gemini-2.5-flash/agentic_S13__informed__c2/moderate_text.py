import os
import requests
from safety_client import get_content_safety_client
from safety_models import ContentSafetyRequest, TextModerationResult

def moderate_text(text: str) -> TextModerationResult:
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
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
        
        # Parse the result into our common model
        moderation_result = TextModerationResult(
            text=text,
            is_unsafe=False,
            categories={}
        )
        if "categoriesAnalysis" in result:
            for category_analysis in result["categoriesAnalysis"]:
                category = category_analysis["category"]
                severity = category_analysis["severity"]
                moderation_result.categories[category] = severity
                if severity > 0: # Any severity greater than 0 indicates some level of unsafety
                    moderation_result.is_unsafe = True
        
        return moderation_result

    except requests.exceptions.RequestException as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        raise
