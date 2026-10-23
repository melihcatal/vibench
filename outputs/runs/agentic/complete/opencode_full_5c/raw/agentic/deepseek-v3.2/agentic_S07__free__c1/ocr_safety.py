import os
from typing import List, Dict, Any, Optional
from google.cloud import language_v1
from document_client import get_language_client
from document_models import OCRResponse


def check_text_safety(ocr_response: OCRResponse) -> dict:
    """Check extracted document text for unsafe content using Google Cloud Natural Language API."""

    client = get_language_client()

    if not ocr_response.text:
        return {
            "is_safe": True,
            "categories": [],
            "confidence": 0.0,
            "provider": "google_cloud_language",
            "model": "content_classification",
        }

    document = language_v1.Document(
        content=ocr_response.text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.classify_text(request={"document": document})

    categories = []
    for category in response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})

    # Check for sensitive categories
    sensitive_categories = [
        "/Law & Government",
        "/Finance",
        "/Health",
        "/Sensitive Subjects",
    ]

    is_safe = True
    for category in categories:
        if any(sensitive in category["name"] for sensitive in sensitive_categories):
            is_safe = False
            break

    return {
        "is_safe": is_safe,
        "categories": categories,
        "confidence": ocr_response.confidence,
        "provider": "google_cloud_language",
        "model": "content_classification",
        "text_length": len(ocr_response.text),
    }


def analyze_sentiment_and_entities(text: str) -> dict:
    """Analyze sentiment and entities in text using Google Cloud Natural Language API."""

    client = get_language_client()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Analyze sentiment
    sentiment_response = client.analyze_sentiment(request={"document": document})
    sentiment = sentiment_response.document_sentiment

    # Analyze entities
    entities_response = client.analyze_entities(request={"document": document})

    entities = []
    for entity in entities_response.entities:
        entities.append(
            {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "mentions": [mention.text.content for mention in entity.mentions],
            }
        )

    # Check for PII (Personally Identifiable Information)
    pii_types = [
        "PERSON",
        "LOCATION",
        "ORGANIZATION",
        "PHONE_NUMBER",
        "EMAIL",
        "ADDRESS",
    ]
    pii_detected = any(entity["type"] in pii_types for entity in entities)

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
        "pii_detected": pii_detected,
        "provider": "google_cloud_language",
        "model": "sentiment_analysis_entity_analysis",
    }


def moderate_content_sections(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Moderate multiple content sections for safety."""

    client = get_language_client()

    moderated_sections = []

    for section in sections:
        text = section.get("text", "")
        if not text:
            moderated_sections.append(
                {**section, "is_safe": True, "moderation_reason": "empty_text"}
            )
            continue

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        try:
            response = client.moderate_text(request={"document": document})

            is_safe = True
            moderation_categories = []

            for category in response.moderation_categories:
                moderation_categories.append(
                    {
                        "name": category.name,
                        "confidence": category.confidence,
                        "flagged": category.confidence > 0.5,  # Threshold for flagging
                    }
                )

                if category.confidence > 0.5:
                    is_safe = False

            moderated_sections.append(
                {
                    **section,
                    "is_safe": is_safe,
                    "moderation_categories": moderation_categories,
                    "provider": "google_cloud_language",
                    "model": "content_moderation",
                }
            )

        except Exception as e:
            moderated_sections.append(
                {**section, "is_safe": False, "moderation_reason": f"error: {str(e)}"}
            )

    return moderated_sections
