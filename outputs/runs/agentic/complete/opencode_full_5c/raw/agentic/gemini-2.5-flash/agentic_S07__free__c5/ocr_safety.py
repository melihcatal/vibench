import os
from google.cloud import language_v1 as language
from document_client import get_language_client
from document_models import SafetyCheckResponse


def check_text_for_safety(text_content: str) -> SafetyCheckResponse:
    client = get_language_client()

    document = language.Document(
        content=text_content, type_=language.Document.Type.PLAIN_TEXT
    )

    # Classify text to detect categories, which can indicate safety concerns
    # Note: For more explicit safety checks, Perspective API or a custom model on Vertex AI would be more direct.
    # This example uses NL API's classification as a proxy for general content assessment.
    response = client.classify_text(request={"document": document})

    safety_attributes = {"categories": []}
    for category in response.categories:
        safety_attributes["categories"].append(
            {"name": category.name, "confidence": category.confidence}
        )

    return SafetyCheckResponse(safety_attributes=safety_attributes)
