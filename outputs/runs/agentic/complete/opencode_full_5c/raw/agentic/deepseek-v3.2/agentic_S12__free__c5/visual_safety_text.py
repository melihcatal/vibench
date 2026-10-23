import os
from google.cloud import language_v1
from typing import List, Dict, Any


def visual_safety_text(labels: List[Dict]) -> Dict[str, Any]:
    """Check generated visual labels for unsafe text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    all_label_text = " ".join([label.get("description", "") for label in labels])

    if not all_label_text.strip():
        return {"is_safe": True, "categories": [], "confidence": 1.0}

    document = language_v1.Document(
        content=all_label_text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    unsafe_categories = []
    for category in response.moderation_categories:
        if category.confidence > 0.5:  # Threshold for considering unsafe
            unsafe_categories.append(
                {"name": category.name, "confidence": category.confidence}
            )

    return {
        "is_safe": len(unsafe_categories) == 0,
        "categories": unsafe_categories,
        "confidence": 1.0
        - max([cat["confidence"] for cat in unsafe_categories], default=0.0),
    }
