from google.cloud import language_v1

from speech_client import get_language_client

def archive_summary(payload: dict):
    client = get_language_client()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)

    # Google Cloud Natural Language API doesn't have a direct summarization API.
    # A common approach for summarization is to extract entities and key phrases
    # or use a more advanced model if available (e.g., via Vertex AI).
    # For the purpose of this exercise and using Natural Language API, we'll extract entities and sentiments
    # as a proxy for summarization, indicating key topics and overall tone.

    # Entity analysis
    entity_response = client.analyze_entities(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8})
    entities = []
    for entity in entity_response.entities:
        entities.append({
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience,
            "mentions": [{
                "text": mention.text.content,
                "type": language_v1.Mention.Type(mention.type_).name
            } for mention in entity.mentions]
        })

    # Sentiment analysis
    sentiment_response = client.analyze_sentiment(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8})
    document_sentiment = {
        "score": sentiment_response.document_sentiment.score,
        "magnitude": sentiment_response.document_sentiment.magnitude
    }

    return {
        "entities": entities,
        "document_sentiment": document_sentiment,
        "summary_note": "Google Cloud Natural Language API does not provide a direct summarization feature. Entities and sentiment are provided as proxies for key information and overall tone."
    }
