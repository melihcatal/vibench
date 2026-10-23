from google.cloud import language_v1

def moderate_text(text_content):
    """Moderates free-text claims or notes using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # Detects entities in the document
    entities = client.analyze_entities(request={"document": document}).entities

    moderation_results = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": [{"name": entity.name, "type": language_v1.Entity.Type(entity.type_).name, "salience": entity.salience} for entity in entities]
    }

    return moderation_results
