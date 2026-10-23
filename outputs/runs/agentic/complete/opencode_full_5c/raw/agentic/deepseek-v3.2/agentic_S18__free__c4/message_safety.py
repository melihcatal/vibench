import os
import json
from typing import Dict, Any, List, Optional
from google.cloud import language_v1


def check_message_safety(text: str, message_id: Optional[str] = None) -> Dict[str, Any]:
    """Check message payload text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    try:
        sentiment_response = client.analyze_sentiment(request={"document": document})

        entities_response = client.analyze_entities(request={"document": document})

        syntax_response = client.analyze_syntax(request={"document": document})

        classification_response = client.classify_text(request={"document": document})
    except Exception as e:
        return {
            "message_id": message_id,
            "safe": False,
            "error": str(e),
            "provider": "google-cloud-language",
        }

    safety_score = calculate_safety_score(
        sentiment_response.document_sentiment,
        entities_response.entities,
        classification_response.categories,
    )

    unsafe_entities = detect_unsafe_entities(entities_response.entities)

    toxic_keywords = check_toxic_keywords(text)

    is_safe = (
        safety_score >= 0.7
        and len(unsafe_entities) == 0
        and len(toxic_keywords) == 0
        and sentiment_response.document_sentiment.score >= -0.5
    )

    return {
        "message_id": message_id,
        "safe": is_safe,
        "safety_score": safety_score,
        "sentiment": {
            "score": sentiment_response.document_sentiment.score,
            "magnitude": sentiment_response.document_sentiment.magnitude,
        },
        "unsafe_entities": unsafe_entities,
        "toxic_keywords": toxic_keywords,
        "categories": [
            {"name": category.name, "confidence": category.confidence}
            for category in classification_response.categories
        ],
        "entity_count": len(entities_response.entities),
        "syntax_tokens": len(syntax_response.tokens),
        "provider": "google-cloud-language",
    }


def calculate_safety_score(sentiment, entities, categories) -> float:
    """Calculate overall safety score from analysis results."""
    score = 0.5

    sentiment_adjustment = (sentiment.score + 1) / 2
    score += sentiment_adjustment * 0.2

    unsafe_entity_count = sum(
        1
        for entity in entities
        if entity.salience > 0.1
        and entity.type_
        in [
            language_v1.Entity.Type.PERSON,
            language_v1.Entity.Type.LOCATION,
            language_v1.Entity.Type.ADDRESS,
            language_v1.Entity.Type.PHONE_NUMBER,
        ]
    )

    if unsafe_entity_count == 0:
        score += 0.2
    elif unsafe_entity_count < 3:
        score += 0.1
    else:
        score -= 0.1

    safe_categories = [
        "/Arts & Entertainment",
        "/Science",
        "/Technology",
        "/Business & Industrial",
    ]
    unsafe_categories = ["/Law & Government", "/Politics", "/Sensitive Subjects"]

    for category in categories:
        if any(safe in category.name for safe in safe_categories):
            score += 0.05 * category.confidence
        elif any(unsafe in category.name for unsafe in unsafe_categories):
            score -= 0.1 * category.confidence

    return max(0.0, min(1.0, score))


def detect_unsafe_entities(entities: List) -> List[Dict[str, Any]]:
    """Detect potentially unsafe entities in text."""
    unsafe_entities = []

    sensitive_types = [
        language_v1.Entity.Type.PERSON,
        language_v1.Entity.Type.LOCATION,
        language_v1.Entity.Type.ADDRESS,
        language_v1.Entity.Type.PHONE_NUMBER,
        language_v1.Entity.Type.NUMBER,
    ]

    for entity in entities:
        if entity.salience > 0.1 and entity.type_ in sensitive_types:
            unsafe_entities.append(
                {
                    "name": entity.name,
                    "type": language_v1.Entity.Type(entity.type_).name,
                    "salience": entity.salience,
                    "metadata": dict(entity.metadata),
                }
            )

    return unsafe_entities


def check_toxic_keywords(text: str) -> List[str]:
    """Check for toxic keywords in text."""
    toxic_patterns = [
        r"\b(hate|kill|murder|attack|violence)\b",
        r"\b(racist|sexist|homophobic|transphobic)\b",
        r"\b(threat|danger|harm|hurt)\b",
        r"\b(abuse|harass|stalk|bully)\b",
    ]

    import re

    found_keywords = []

    for pattern in toxic_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found_keywords.extend(matches)

    return list(set(found_keywords))


def batch_check_safety(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Batch check multiple messages for safety."""
    results = []
    unsafe_count = 0

    for message in messages:
        text = message.get("text", "")
        if isinstance(message, dict) and "text" not in message:
            text = json.dumps(message)

        message_id = message.get("message_id", message.get("id", None))

        safety_result = check_message_safety(text, message_id)
        results.append(safety_result)

        if not safety_result["safe"]:
            unsafe_count += 1

    return {
        "total_messages": len(messages),
        "safe_messages": len(messages) - unsafe_count,
        "unsafe_messages": unsafe_count,
        "safety_rate": (len(messages) - unsafe_count) / len(messages)
        if len(messages) > 0
        else 1.0,
        "results": results,
        "provider": "google-cloud-language",
    }


def create_safety_policy(violation_threshold: int = 3) -> Dict[str, Any]:
    """Create a safety policy configuration."""
    return {
        "violation_threshold": violation_threshold,
        "auto_quarantine": True,
        "notify_on_violation": True,
        "check_categories": ["sentiment", "entities", "toxicity", "pii"],
        "minimum_safety_score": 0.7,
        "maximum_negative_sentiment": -0.5,
        "provider": "google-cloud-language",
    }


if __name__ == "__main__":
    test_text = "This is a friendly message about technology and science."
    safety_result = check_message_safety(test_text, "test_123")
    print(f"Safety check result: {json.dumps(safety_result, indent=2)}")
