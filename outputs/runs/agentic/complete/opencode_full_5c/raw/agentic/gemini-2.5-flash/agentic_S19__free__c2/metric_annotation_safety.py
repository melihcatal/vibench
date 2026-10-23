from google.cloud import language_v1
from observability_client import get_language_client
from observability_models import AnalyzeContentResponse, DocumentSentiment, Entity


def check_annotation_safety(text: str) -> AnalyzeContentResponse:
    client = get_language_client()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detect sentiment
    sentiment_response = client.analyze_sentiment(document=document)
    doc_sentiment = DocumentSentiment(
        score=sentiment_response.document_sentiment.score,
        magnitude=sentiment_response.document_sentiment.magnitude,
    )

    # Detect entities
    entity_response = client.analyze_entities(
        document=document, encoding_type=language_v1.EncodingType.UTF8
    )
    entities = []
    for entity in entity_response.entities:
        entity_sentiment = None
        if entity.sentiment:
            entity_sentiment = DocumentSentiment(
                score=entity.sentiment.score, magnitude=entity.sentiment.magnitude
            )
        entities.append(
            Entity(
                name=entity.name,
                type=entity.type_,
                salience=entity.salience,
                sentiment=entity_sentiment,
            )
        )

    return AnalyzeContentResponse(sentiment=doc_sentiment, entities=entities)


if __name__ == "__main__":
    test_text_safe = "The system is running perfectly, no issues detected."
    test_text_unsafe = "This dashboard looks terrible and is completely broken!"

    print("\n--- Safe Text Analysis ---")
    safe_analysis = check_annotation_safety(test_text_safe)
    print(
        f"Document Sentiment: Score={safe_analysis.sentiment.score:.2f}, Magnitude={safe_analysis.sentiment.magnitude:.2f}"
    )
    print("Entities:")
    for entity in safe_analysis.entities:
        print(
            f"  Name: {entity.name}, Type: {entity.type}, Salience: {entity.salience:.2f}"
        )

    print("\n--- Unsafe Text Analysis ---")
    unsafe_analysis = check_annotation_safety(test_text_unsafe)
    print(
        f"Document Sentiment: Score={unsafe_analysis.sentiment.score:.2f}, Magnitude={unsafe_analysis.sentiment.magnitude:.2f}"
    )
    print("Entities:")
    for entity in unsafe_analysis.entities:
        print(
            f"  Name: {entity.name}, Type: {entity.type}, Salience: {entity.salience:.2f}"
        )
