from google.cloud import language


def asset_metadata_embedding(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    embedding = client.analyze_entity_sentiment(document).entities

    for entity in embedding:
        print(f"Entity: {entity.name}, Sentiment: {entity.sentiment.score}")

    return embedding
