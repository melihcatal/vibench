from google.cloud import language_v1


def summarize_translation_quality(translated_text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=translated_text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    # Detects entities in the text
    entities_response = client.analyze_entities(request={"document": document})
    entities = [
        {
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience,
        }
        for entity in entities_response.entities
    ]

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
        "quality_summary": (
            "The translated text generally conveys a neutral to positive sentiment. "
            f"Sentiment Score: {sentiment.score:.2f}, Magnitude: {sentiment.magnitude:.2f}. "
            "Entities detected provide context on key subjects mentioned."  # Model family / model identifier not directly applicable here. Provider signal is google.cloud.language_v1
        ),
    }
