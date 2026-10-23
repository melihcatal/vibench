from google.cloud import language_v1
from typing import Dict, Any, List


def check_unsafe_content(text: str) -> Dict[str, Any]:
    """Checks localized copy for potentially unsafe content using Google Cloud Natural Language API.

    This function performs entity and sentiment analysis, which can be used as indicators
    for further review of content for safety and appropriateness. It is not a direct
    content moderation tool but provides signals.

    Args:
        text: The localized text to check.

    Returns:
        A dictionary containing analysis results, including entities and sentiment.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform entity analysis
    entities_response = client.analyze_entities(request={"document": document})
    entities_info = []
    for entity in entities_response.entities:
        entities_info.append(
            {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "mentions": [mention.text.content for mention in entity.mentions],
            }
        )

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(request={"document": document})
    sentiment_info = {
        "score": sentiment_response.document_sentiment.score,
        "magnitude": sentiment_response.document_sentiment.magnitude,
    }

    return {
        "entities": entities_info,
        "sentiment": sentiment_info,
        "note": "Review entities and sentiment for potential safety flags. For direct content moderation, consider Google Cloud's Perspective API.",
    }
