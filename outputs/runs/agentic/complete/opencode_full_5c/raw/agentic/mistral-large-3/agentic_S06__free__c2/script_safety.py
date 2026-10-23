from google.cloud import language_v1 as language
import os


def check_script_safety(text: str) -> dict:
    client = language.LanguageServiceClient()

    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(request={"document": document})

    sentiment = response.document_sentiment

    response = client.analyze_entity_sentiment(request={"document": document})

    entities = []
    for entity in response.entities:
        entities.append(
            {
                "name": entity.name,
                "type": language.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "sentiment": {
                    "score": entity.sentiment.score,
                    "magnitude": entity.sentiment.magnitude,
                },
            }
        )

    return {
        "sentiment": {"score": sentiment.score, "magnitude": sentiment.magnitude},
        "entities": entities,
    }
