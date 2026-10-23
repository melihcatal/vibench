from google.cloud import language_v1

def moderate_claims_text(text_content: str) -> dict:
    """
    Moderates free-text claims or notes using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect sentiment
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    print(f"Text: {text_content}")
    print(f"Sentiment: score={sentiment.score}, magnitude={sentiment.magnitude}")

    # Detect entities
    entities = client.analyze_entities(request={'document': document}).entities
    entity_mentions = []
    for entity in entities:
        entity_mentions.append({
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience,
            "wikipedia_url": entity.metadata.get('wikipedia_url', 'N/A'),
            "mentions": [{'text': mention.text.content, 'type': language_v1.EntityMention.Type(mention.type_).name} for mention in entity.mentions]
        })

    print("Entities:")
    for entity in entity_mentions:
        print(f"  Name: {entity["name"]}, Type: {entity["type"]}, Salience: {entity["salience"]}")

    return {
        "sentiment": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        },
        "entities": entity_mentions
    }
