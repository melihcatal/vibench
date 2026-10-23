import os
from google.cloud import language_v1


def check_narration_safety(text):
    """Check narration scripts for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_sentiment(request={"document": document})

    safety_issues = []

    if response.document_sentiment.score < -0.5:
        safety_issues.append("Highly negative sentiment detected")

    if response.document_sentiment.magnitude > 2.0:
        safety_issues.append("Strong emotional content detected")

    try:
        classify_response = client.classify_text(request={"document": document})

        for category in classify_response.categories:
            if "sensitive" in category.name.lower() or "adult" in category.name.lower():
                safety_issues.append(f"Potentially sensitive category: {category.name}")
    except:
        pass

    analyze_entities_response = client.analyze_entities(request={"document": document})

    sensitive_entities = ["weapon", "violence", "drug", "alcohol", "tobacco"]
    for entity in analyze_entities_response.entities:
        entity_type = language_v1.Entity.Type(entity.type_).name
        if any(sensitive in entity_type.lower() for sensitive in sensitive_entities):
            safety_issues.append(
                f"Sensitive entity detected: {entity.name} ({entity_type})"
            )

    return {
        "is_safe": len(safety_issues) == 0,
        "safety_issues": safety_issues,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
    }
