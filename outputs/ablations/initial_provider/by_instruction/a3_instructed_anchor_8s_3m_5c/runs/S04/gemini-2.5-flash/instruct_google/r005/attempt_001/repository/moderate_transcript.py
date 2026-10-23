from google.cloud import language_v1
from typing import List

def moderate_transcript_text(text: str) -> dict:
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Classify text into categories to identify potentially harmful content
    # Note: This is a basic classification. For robust moderation, a more advanced solution
    # with custom models or dedicated moderation APIs might be needed.
    response = client.classify_text(request={'document': document})
    
    categories = []
    for category in response.categories:
        categories.append({
            "name": category.name,
            "confidence": category.confidence,
        })
        
    # You might also consider using the client.analyze_sentiment(document=document) for sentiment analysis
    # as part of moderation, but classify_text is a better fit for content categorization.

    return {"categories": categories}
