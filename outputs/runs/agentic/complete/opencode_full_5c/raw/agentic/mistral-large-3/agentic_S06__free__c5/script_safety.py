from google.cloud import language_v1 as language
from typing import List, Dict


def analyze_script_safety(text: str) -> Dict:
    """
    Checks narration scripts for unsafe content using Google Cloud Natural Language API.
    """
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
                "sentiment": {
                    "score": entity.sentiment.score,
                    "magnitude": entity.sentiment.magnitude,
                },
            }
        )

    response = client.classify_text(request={"document": document})

    categories = []
    for category in response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})

    return {
        "sentiment": {"score": sentiment.score, "magnitude": sentiment.magnitude},
        "entities": entities,
        "categories": categories,
    }


def is_script_unsafe(
    text: str, sentiment_threshold: float = -0.5, category_threshold: float = 0.8
) -> bool:
    """
    Determines if a script is unsafe based on sentiment and content categories.
    """
    analysis = analyze_script_safety(text)

    if analysis["sentiment"]["score"] < sentiment_threshold:
        return True

    for category in analysis["categories"]:
        if category["confidence"] >= category_threshold and (
            "Adult" in category["name"]
            or "Violence" in category["name"]
            or "Toxic" in category["name"]
        ):
            return True

    return False
