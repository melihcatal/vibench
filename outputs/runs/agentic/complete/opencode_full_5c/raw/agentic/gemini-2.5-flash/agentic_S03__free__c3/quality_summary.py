from google.cloud import language_v1
from typing import Dict


def analyze_translation_quality(text: str) -> Dict[str, Any]:
    """Analyzes the sentiment of a translated text to give a proxy for quality.

    Args:
        text: The translated text to analyze.

    Returns:
        A dictionary containing sentiment score and magnitude.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "summary": "Positive sentiment indicates potentially good quality, negative for poor quality.",
    }
