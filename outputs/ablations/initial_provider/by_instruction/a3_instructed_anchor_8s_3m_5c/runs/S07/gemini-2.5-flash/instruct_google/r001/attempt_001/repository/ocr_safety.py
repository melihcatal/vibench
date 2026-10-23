from document_client import get_language_client
from document_models import DocumentSafety, SafetyScore
from google.cloud import language_v1

def check_safety(text_content: str) -> DocumentSafety:
    client = get_language_client()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories for content classification. Check the official documentation for the latest list.
    response = client.classify_text(request={'document': document})

    safety_scores = []
    for category in response.categories:
        # Google Cloud Natural Language API classification doesn't directly provide 'safety scores' in the same way
        # a dedicated moderation API might. Instead, it provides a confidence score for each category.
        # For demonstration purposes, we'll map category names to a simplified safety score model.
        # A real safety check would involve more sophisticated logic or a dedicated content moderation API like Perspective API.
        safety_scores.append(SafetyScore(category=category.name, score=category.confidence))
    
    return DocumentSafety(safety_scores=safety_scores)
