import os
import httpx
from messaging_client import get_azure_content_safety_client
from messaging_models import EventMessage, SafetyCheckResult
import json


def check_message_safety(message: EventMessage) -> SafetyCheckResult:
    client = get_azure_content_safety_client()

    # Extract relevant text content from the message for safety check
    text_content = json.dumps(
        message.data
    )  # Assuming message.data contains the main content to check

    body = {
        "text": text_content,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "blocklistNames": [],
        "breakdown": True,
    }

    response = client.post(
        "/contentsafety/text:analyze?api-version=2023-10-15-preview", json=body
    )
    response.raise_for_status()  # Raise an exception for HTTP errors

    moderation_results = response.json()

    # Determine if content is safe based on moderation results
    is_safe = True
    for category_result in moderation_results.get("categoriesAnalysis", []):
        if category_result.get("severity") and category_result["severity"] > 0:
            is_safe = False
            break

    return SafetyCheckResult(is_safe=is_safe, moderation_results=moderation_results)


if __name__ == "__main__":
    pass
