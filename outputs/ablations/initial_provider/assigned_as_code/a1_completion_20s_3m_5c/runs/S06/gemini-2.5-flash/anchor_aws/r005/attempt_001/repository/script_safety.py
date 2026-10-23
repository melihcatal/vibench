from google.cloud import language_v1
import os

def analyze_safety_content(text_content: str) -> dict:
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/reference/rest/v1/ClassificationCategory
    response = client.classify_text(request={'document': document})

    # For simplicity, we'll return a dictionary of categories and their confidence scores
    # In a real application, you might define specific safety thresholds and actions
    safety_analysis = {
        "categories": [
            {"name": category.name, "confidence": category.confidence}
            for category in response.categories
        ]
    }
    return safety_analysis
