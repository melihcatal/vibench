import os
import requests
from speech_models import ModerationRequest, ModerationResult


def moderate_text(request: ModerationRequest) -> ModerationResult:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not configured.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

    payload = {
        "text": request.text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "breakByBlocklists": True,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    is_safe = all(
        category.get("severity", 0) == 0
        for category in result.get("categoriesAnalysis", [])
    )

    return ModerationResult(is_safe=is_safe, categories=result)
