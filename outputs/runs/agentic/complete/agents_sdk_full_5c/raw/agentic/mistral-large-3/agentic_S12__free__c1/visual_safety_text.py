import os
from typing import List
from google.cloud import language_v1
from vision_models import SafetyTextResponse


def check_visual_labels_for_unsafe_text(labels: List[str]) -> SafetyTextResponse:
    """Checks generated visual labels for unsafe text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    
    text = " ".join(labels)
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    response = client.moderate_text(document=document)
    
    unsafe_categories = []
    for category in response.moderation_categories:
        if category.confidence > 0.7:
            unsafe_categories.append(category.name)
    
    return SafetyTextResponse(
        provider="google_cloud_natural_language",
        is_unsafe=len(unsafe_categories) > 0,
        unsafe_categories=unsafe_categories
    )