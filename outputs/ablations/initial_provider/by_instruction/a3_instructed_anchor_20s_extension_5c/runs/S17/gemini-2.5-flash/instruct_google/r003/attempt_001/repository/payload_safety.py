from google.cloud import language_v1
from security_client import NaturalLanguageClientWrapper

def check_payload_safety(text_payload: str) -> dict:
    """Checks decrypted text payloads for unsafe content using Google Cloud Natural Language API.

    This function performs sentiment analysis and entity extraction to provide a basic
    safety assessment of the text content.

    Args:
        text_payload: The decrypted text content to check.

    Returns:
        A dictionary containing the sentiment score, magnitude, and detected entities.
    """
    client_wrapper = NaturalLanguageClientWrapper()
    client = client_wrapper.client

    document = language_v1.Document(
        content=text_payload, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(request={"document": document})
    sentiment = sentiment_response.document_sentiment

    # Perform entity analysis
    entity_response = client.analyze_entities(request={"document": document})
    entities = []
    for entity in entity_response.entities:
        entities.append({
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience,
            "mentions": [mention.text.content for mention in entity.mentions]
        })

    safety_report = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
    }

    return safety_report
