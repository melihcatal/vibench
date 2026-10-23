from google.cloud import language_v1 as language

def check_caption_for_safety(text_content: str) -> dict:
    """
    Checks live transcript text for unsafe content using Google Cloud Natural Language API.
    This function uses sentiment analysis as a basic proxy for "safety" given the API capabilities.
    For true content moderation, a dedicated moderation API (like Google Cloud's content moderation features
    in Vertex AI or a third-party service) would be more appropriate.
    """
    client = language.LanguageServiceClient()

    document = language.Document(content=text_content, type_=language.Document.Type.PLAIN_TEXT)
    
    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(request={'document': document})
    sentiment = sentiment_response.document_sentiment

    # Perform entity analysis for potential keywords (optional, for broader "safety" check)
    # entity_response = client.analyze_entities(request={'document': document})
    # entities = entity_response.entities

    safety_score = {
        "magnitude": sentiment.magnitude,
        "score": sentiment.score,
        "assessment": "Neutral" # Default
    }

    if sentiment.score < -0.2: # Arbitrary threshold for negative sentiment
        safety_score["assessment"] = "Potentially Negative/Unsafe"
    elif sentiment.score > 0.2: # Arbitrary threshold for positive sentiment
        safety_score["assessment"] = "Positive/Safe"
    
    return safety_score
