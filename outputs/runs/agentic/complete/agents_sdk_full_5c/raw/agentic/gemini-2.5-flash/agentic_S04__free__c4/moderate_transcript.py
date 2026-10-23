from google.cloud import language_v1

def moderate_transcript_text(text_content: str):
    """
    Moderates transcript text using Google Cloud Natural Language API (sentiment and entity analysis as proxies).
    For direct content moderation, consider a specialized content moderation API if available.

    Args:
        text_content: The full transcript text to moderate.

    Returns:
        A dictionary containing sentiment score, magnitude, and detected entities.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.types.Document(
        content=text_content, type=language_v1.types.Document.Type.PLAIN_TEXT
    )

    sentiment = client.analyze_sentiment(document=document).document_sentiment
    entities = client.analyze_entities(document=document).entities

    print("Transcript text analyzed for moderation (sentiment and entities).")
    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": [{"name": entity.name, "type": language_v1.types.Entity.Type(entity.type_).name} for entity in entities]
    }
