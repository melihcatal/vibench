from google.cloud import language_v1

def check_text_safety(text_content: str) -> dict:
    """
    Checks text for safety using Google Cloud Natural Language API.

    Args:
        text_content: The text to analyze.

    Returns:
        A dictionary containing the sentiment and entity analysis results.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Perform entity analysis
    entities = client.analyze_entities(request={'document': document}).entities

    return {
        "sentiment": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude,
        },
        "entities": [{
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience
        } for entity in entities]
    }
