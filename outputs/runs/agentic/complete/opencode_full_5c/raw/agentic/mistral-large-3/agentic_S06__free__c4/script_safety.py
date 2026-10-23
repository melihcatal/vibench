from google.cloud import language_v1 as language
from typing import List, Dict


def analyze_script_safety(text: str) -> Dict:
    client = language.LanguageServiceClient()
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
                "sentiment": entity.sentiment.score,
            }
        )

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
    }


def check_script_unsafe_content(text: str, threshold: float = -0.5) -> bool:
    analysis = analyze_script_safety(text)
    return analysis["sentiment_score"] < threshold
