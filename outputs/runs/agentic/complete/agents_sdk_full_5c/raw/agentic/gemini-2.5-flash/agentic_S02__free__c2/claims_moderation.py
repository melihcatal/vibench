import os
from google.cloud import language_v1
from typing import Dict, Any, List

# Google Cloud Natural Language API for content moderation
# Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set

language_client = language_v1.LanguageServiceClient()

def moderate_text_claims(text: str) -> Dict[str, Any]:
    """Analyzes text for sentiment and entities, useful for moderation."""
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    sentiment_response = language_client.analyze_sentiment(document=document, encoding_type=language_v1.EncodingType.UTF8)
    entity_response = language_client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)
    
    # Also consider content classification for broader moderation
    # Note: Classification requires a minimum text length (20 words) and is not always suitable for short claims.
    # For demonstration, we'll keep it simple with sentiment and entities.
    # classification_response = language_client.classify_text(document=document)

    result = {
        "original_text": text,
        "sentiment": {
            "score": sentiment_response.document_sentiment.score,
            "magnitude": sentiment_response.document_sentiment.magnitude,
        },
        "entities": [{
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience,
            "sentiment": {
                "score": entity.sentiment.score,
                "magnitude": entity.sentiment.magnitude,
            } if entity.sentiment else None,
        } for entity in entity_response.entities],
        # "categories": [c.name for c in classification_response.categories] # if enabled
    }
    return result

def check_for_inappropriate_content(moderation_result: Dict[str, Any], sentiment_threshold: float = -0.5) -> bool:
    """A simple heuristic to check for potentially inappropriate content based on sentiment."""
    if moderation_result["sentiment"]["score"] < sentiment_threshold:
        return True
    return False

if __name__ == "__main__":
    # Example free-text claims or notes
    example_claims = [
        "This user consistently provides positive feedback on new features.",
        "There was an issue with the login flow, very frustrating user experience.",
        "User complained about slow performance. Please investigate.",
        "Great service, thank you!"
    ]

    print("Moderating example claims using Google Cloud Natural Language API...")
    for claim in example_claims:
        print(f"\nProcessing claim: \'{claim}\'")
        moderation_output = moderate_text_claims(claim)
        print(f"  Sentiment Score: {moderation_output["sentiment"]["score"]:.2f}, Magnitude: {moderation_output["sentiment"]["magnitude"]:.2f}")
        print(f"  Entities: {[e['name'] for e in moderation_output["entities"]]}")
        if check_for_inappropriate_content(moderation_output):
            print("  -> Flagged as potentially inappropriate!")
        else:
            print("  -> Appears appropriate.")
