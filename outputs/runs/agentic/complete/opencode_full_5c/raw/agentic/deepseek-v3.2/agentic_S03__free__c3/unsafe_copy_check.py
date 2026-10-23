import os
from typing import Dict, List, Any
from google.cloud import language_v1


def check_localized_copy_for_unsafe_content(
    text: str, language_code: str
) -> Dict[str, Any]:
    """
    Check localized copy for unsafe content using Google Cloud Natural Language API.

    Args:
        text: Text to analyze for unsafe content
        language_code: Language code of the text

    Returns:
        Dictionary with safety analysis results
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language=language_code
    )

    # Analyze sentiment as a proxy for emotional safety
    sentiment_response = client.analyze_sentiment(request={"document": document})

    # Analyze entities for potentially sensitive content
    entity_response = client.analyze_entities(request={"document": document})

    # Analyze syntax for potential issues
    syntax_response = client.analyze_syntax(request={"document": document})

    # Check for potentially unsafe entities
    unsafe_entities = []
    for entity in entity_response.entities:
        if entity.salience > 0.1:  # High salience entities
            entity_info = {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
            }
            unsafe_entities.append(entity_info)

    # Analyze sentiment scores
    sentiment = sentiment_response.document_sentiment

    # Determine safety level based on sentiment and entities
    is_safe = True
    safety_issues = []

    if sentiment.score < -0.5:
        is_safe = False
        safety_issues.append("Highly negative sentiment detected")

    if sentiment.magnitude > 2.0:
        safety_issues.append("High emotional intensity detected")

    return {
        "is_safe": is_safe,
        "safety_issues": safety_issues,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "unsafe_entities": unsafe_entities,
        "language_code": language_code,
        "provider": "Google Cloud Natural Language API",
    }
