from google.cloud import language_v1 as language
import os
from typing import List
from document_client import get_document_client, load_config
from document_models import SafetyResponse


def check_ocr_safety(text: str) -> SafetyResponse:
    """
    Checks extracted OCR text for unsafe content using Google Cloud Natural Language API.

    Args:
        text: The text extracted from OCR to check for safety.

    Returns:
        SafetyResponse indicating whether the text is safe and unsafe categories.
    """
    client = language.LanguageServiceClient()
    config = load_config("google")

    project_id = config.get("project_id")

    if not project_id:
        raise ValueError(
            "Google Cloud project ID must be set in environment variables."
        )

    document = {"content": text, "type_": language.Document.Type.PLAIN_TEXT}

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment

    # Check for toxic content using sentiment and magnitude
    is_safe = True
    unsafe_categories = []

    if sentiment.score < -0.5 and sentiment.magnitude > 0.5:
        is_safe = False
        unsafe_categories.append("toxic_language")

    # Additional check for explicit content
    response = client.classify_text(
        request={
            "document": document,
            "classification_model_options": {
                "v2_model": {"content_categories_version": "V2"}
            },
        }
    )

    for category in response.categories:
        if category.confidence > 0.7 and (
            "Adult" in category.name
            or "Violence" in category.name
            or "Racism" in category.name
        ):
            is_safe = False
            unsafe_categories.append(category.name)

    return SafetyResponse(
        is_safe=is_safe,
        unsafe_categories=unsafe_categories,
        confidence=1.0 - sentiment.magnitude if sentiment.magnitude < 1.0 else 0.0,
        provider="google_cloud_natural_language",
        model="v1",
    )
