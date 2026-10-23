import os
from google.cloud import language_v2 as language
from google.cloud.language_v2 import Document, DocumentSentiment, AnnotateTextRequest

def profile_moderation(profile_text: str) -> dict:
    client = language.LanguageServiceClient()

    document = Document(content=profile_text, type_=language.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis and entity analysis (for content categorization/moderation context)
    response = client.annotate_text(
        request={
            "document": document,
            "features": {
                "extract_sentiment": True,
                "extract_entities": True,
                "classify_text": True # For content classification
            },
            "encoding_type": language.EncodingType.UTF8,
        }
    )

    # Basic moderation check: looking for highly negative sentiment or specific categories
    sentiment_score = response.document_sentiment.score
    sentiment_magnitude = response.document_sentiment.magnitude
    
    moderation_flags = []
    if sentiment_score < -0.5 and sentiment_magnitude > 1.0: # Arbitrary threshold for strong negative sentiment
        moderation_flags.append("STRONG_NEGATIVE_SENTIMENT")

    # Classify text can give insights into content. For moderation, specific categories might be flagged.
    # This is a placeholder for more advanced moderation logic based on categories.
    categories = []
    if response.categories:
        for category in response.categories:
            categories.append({"name": category.name, "confidence": category.confidence})
            # Example: if '/Computers & Electronics' in category.name and category.confidence > 0.8:
            #   moderation_flags.append('TECH_RELATED_SPAM_POSSIBLE')

    entities = []
    if response.entities:
        for entity in response.entities:
            entities.append({"name": entity.name, "type": entity.type_.name})

    is_flagged = bool(moderation_flags)

    return {
        "profile_text": profile_text,
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
        "moderation_flags": moderation_flags,
        "is_flagged_for_review": is_flagged,
        "categories": categories,
        "entities": entities
    }
