import os
from google.cloud import language_v1
from typing import Dict, Any
from messaging_models import PubsubMessage


def check_message_safety(message: PubsubMessage) -> Dict[str, Any]:
    """Checks message payload text for unsafe content using Google Cloud Natural Language API.

    The message payload is expected to have a 'text' field.
    """
    client = language_v1.LanguageServiceClient()
    text_content = message.data.get("text", "")

    if not text_content:
        return {"safe": True, "details": "No text content to analyze."}

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Classify text content for safety attributes
    # Model identifiable by `google.cloud.language_v1` and API endpoint implicitly used by client.
    # The specific model used for content classification is managed by the Google Cloud Natural Language API service.
    response = client.classify_text(request={"document": document})

    # Look for categories indicating unsafe content
    # This is a simplification; actual safety classification would be more nuanced.
    unsafe_categories = ["/Bias", "/Hate Speech", "/Threat"]
    is_safe = True
    safety_details = []

    for category in response.categories:
        if (
            category.name in unsafe_categories and category.confidence > 0.5
        ):  # Example confidence threshold
            is_safe = False
            safety_details.append(
                {"category": category.name, "confidence": category.confidence}
            )

    return {
        "safe": is_safe,
        "details": safety_details if safety_details else "Content appears safe.",
    }
