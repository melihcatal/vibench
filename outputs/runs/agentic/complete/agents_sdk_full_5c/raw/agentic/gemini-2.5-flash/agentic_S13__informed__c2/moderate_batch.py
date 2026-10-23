import os
import requests
from typing import List
from safety_client import get_content_safety_client
from safety_models import TextModerationResult

def moderate_batch(texts: List[str]) -> List[TextModerationResult]:
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    Note: Azure AI Content Safety API typically processes one text at a time. 
    This implementation will iterate through the batch, making individual calls.
    For true batch processing, a custom wrapper or different service might be needed.
    """
    client = get_content_safety_client()
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    all_results: List[TextModerationResult] = []
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    for text in texts:
        payload = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels"
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
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
                    if severity > 0: 
                        moderation_result.is_unsafe = True
            all_results.append(moderation_result)

        except requests.exceptions.RequestException as e:
            print(f"Error moderating text '{text}' with Azure AI Content Safety: {e}")
            # Append a default or error result for this specific text
            all_results.append(TextModerationResult(text=text, is_unsafe=True, categories={"Error": 1}))
            
    return all_results
