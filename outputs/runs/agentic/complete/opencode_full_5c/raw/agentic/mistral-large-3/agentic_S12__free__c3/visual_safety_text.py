import os
from google.cloud import language_v1
from typing import Dict, List
from .vision_models import VisualSafetyTextRequest


def check_visual_safety_text(request: VisualSafetyTextRequest) -> Dict:
    """Checks generated visual labels for unsafe text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    unsafe_categories = []
    for text in request.texts:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.classify_text(document=document)

        for category in response.categories:
            if category.confidence > 0.7 and any(
                keyword in category.name.lower()
                for keyword in ["violence", "drugs", "hate", "sexual", "weapons"]
            ):
                unsafe_categories.append(
                    {
                        "text": text,
                        "category": category.name,
                        "confidence": category.confidence,
                    }
                )

    return {
        "provider": "google_cloud_natural_language",
        "model": "classify_text",
        "unsafe_texts": unsafe_categories,
    }
