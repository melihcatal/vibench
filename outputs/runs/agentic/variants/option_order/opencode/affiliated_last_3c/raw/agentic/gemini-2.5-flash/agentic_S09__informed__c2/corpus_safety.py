import os
import requests
import json
from embeddings_models import ContentSafetyRequest, ContentSafetyResponse


def check_corpus_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    """
    Checks corpus text for safety using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": request.text}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Basic safety check: if any category has a high severity, consider it unsafe
        is_safe = True
        for category in result.get("categoriesAnalysis", []):
            if (
                category.get("severity", 0) >= 2
            ):  # Severity 2 or higher usually indicates potential harm
                is_safe = False
                break

        return ContentSafetyResponse(is_safe=is_safe, moderation_results=result)
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety: {e}")
        return ContentSafetyResponse(
            is_safe=False, moderation_results={"error": str(e)}
        )
