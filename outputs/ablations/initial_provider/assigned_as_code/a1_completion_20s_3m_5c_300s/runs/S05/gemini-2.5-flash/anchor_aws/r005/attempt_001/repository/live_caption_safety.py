from google.cloud import language_v1
from google.cloud.language_v1 import types
import os

def analyze_safety(text_content: str) -> dict:
    """Checks text content for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = types.Document(
        content=text_content, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories are: 'Toxicity', 'Sexually Explicit', 'Flirtation', etc.
    # The API might evolve, so refer to the latest documentation for a complete list.
    response = client.classify_text(request={'document': document})

    safety_scores = {}
    for category in response.categories:
        # The name of the category (e.g., '/Toxicity')
        category_name = category.name.split('/')[-1] 
        # The confidence score for the category
        safety_scores[category_name] = category.confidence

    # For this example, we consider content unsafe if any category has a high confidence.
    # Thresholds would typically be defined based on application requirements.
    is_unsafe = False
    unsafe_categories = []
    for category, confidence in safety_scores.items():
        if confidence > 0.7:  # Example threshold
            is_unsafe = True
            unsafe_categories.append(category)

    return {
        "text": text_content,
        "is_unsafe": is_unsafe,
        "unsafe_categories": unsafe_categories,
        "safety_scores": safety_scores,
    }
