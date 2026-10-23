import os
import json
from typing import Dict, Any, List
from google.cloud import language_v1


def check_message_safety(message_data, language="en"):
    """Check message payload text for unsafe content using Google Cloud Natural Language API."""

    # Initialize the Natural Language API client
    client = language_v1.LanguageServiceClient()

    # Extract text from message data
    text_to_analyze = extract_text_from_message(message_data)

    if not text_to_analyze:
        return {
            "safe": True,
            "reason": "No text content to analyze",
            "checks_performed": [],
            "provider": "google_cloud_natural_language",
        }

    # Prepare the document
    document = language_v1.Document(
        content=text_to_analyze,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language=language,
    )

    # Analyze sentiment (for overall tone)
    sentiment_response = client.analyze_sentiment(request={"document": document})

    # Analyze entities (for sensitive information)
    entity_response = client.analyze_entities(request={"document": document})

    # Analyze syntax (for structure)
    syntax_response = client.analyze_syntax(request={"document": document})

    # Check for safety issues
    safety_issues = []

    # 1. Check for highly negative sentiment
    if sentiment_response.document_sentiment.score < -0.7:
        safety_issues.append(
            {
                "type": "highly_negative_sentiment",
                "score": sentiment_response.document_sentiment.score,
                "severity": "medium",
            }
        )

    # 2. Check for highly negative magnitude (emotional intensity)
    if sentiment_response.document_sentiment.magnitude > 2.0:
        safety_issues.append(
            {
                "type": "high_emotional_intensity",
                "magnitude": sentiment_response.document_sentiment.magnitude,
                "severity": "low",
            }
        )

    # 3. Check for sensitive entities
    sensitive_entities = []
    for entity in entity_response.entities:
        if entity.salience > 0.1:  # Highly salient entities
            entity_type = language_v1.Entity.Type(entity.type_).name
            if entity_type in [
                "PERSON",
                "LOCATION",
                "ADDRESS",
                "PHONE_NUMBER",
                "PRICE",
            ]:
                sensitive_entities.append(
                    {
                        "name": entity.name,
                        "type": entity_type,
                        "salience": entity.salience,
                    }
                )

    if sensitive_entities:
        safety_issues.append(
            {
                "type": "sensitive_entities",
                "entities": sensitive_entities,
                "severity": "high",
            }
        )

    # 4. Check for profanity or offensive words (basic check)
    offensive_words = check_for_offensive_words(text_to_analyze)
    if offensive_words:
        safety_issues.append(
            {"type": "offensive_language", "words": offensive_words, "severity": "high"}
        )

    # 5. Check text length (very short or very long messages might be suspicious)
    word_count = len(text_to_analyze.split())
    if word_count < 3:
        safety_issues.append(
            {"type": "very_short_message", "word_count": word_count, "severity": "low"}
        )
    elif word_count > 1000:
        safety_issues.append(
            {"type": "very_long_message", "word_count": word_count, "severity": "low"}
        )

    # Determine overall safety
    high_severity_issues = [
        issue for issue in safety_issues if issue["severity"] == "high"
    ]
    medium_severity_issues = [
        issue for issue in safety_issues if issue["severity"] == "medium"
    ]

    is_safe = len(high_severity_issues) == 0

    result = {
        "safe": is_safe,
        "text_analyzed": text_to_analyze[:500]
        + ("..." if len(text_to_analyze) > 500 else ""),
        "safety_issues": safety_issues,
        "sentiment": {
            "score": sentiment_response.document_sentiment.score,
            "magnitude": sentiment_response.document_sentiment.magnitude,
        },
        "entity_count": len(entity_response.entities),
        "word_count": word_count,
        "checks_performed": [
            "sentiment_analysis",
            "entity_analysis",
            "syntax_analysis",
            "offensive_language_check",
            "length_check",
        ],
        "provider": "google_cloud_natural_language",
        "model": "natural-language-api-v1",
    }

    if not is_safe:
        result["block_reason"] = "Contains high severity safety issues"
        result["recommended_action"] = (
            "Review message manually or send to moderation queue"
        )

    return result


def extract_text_from_message(message_data):
    """Extract text content from message data."""
    if isinstance(message_data, str):
        return message_data
    elif isinstance(message_data, dict):
        # Try to find text fields
        text_fields = ["text", "content", "message", "body", "description", "comment"]
        for field in text_fields:
            if field in message_data and isinstance(message_data[field], str):
                return message_data[field]

        # If no text field found, convert dict to string
        return json.dumps(message_data)
    else:
        return str(message_data)


def check_for_offensive_words(text):
    """Basic check for offensive words (simplified for example)."""
    offensive_word_list = [
        # This would be a more comprehensive list in production
        "badword1",
        "badword2",
        "offensive1",
    ]

    text_lower = text.lower()
    found_words = []

    for word in offensive_word_list:
        if word in text_lower:
            found_words.append(word)

    return found_words


def should_block_message(message_data, safety_threshold="medium"):
    """Determine if message should be blocked based on safety check."""
    safety_result = check_message_safety(message_data)

    if not safety_result["safe"]:
        return True, safety_result

    # Additional threshold-based checking
    if safety_threshold == "high":
        # High threshold: block even medium severity issues
        medium_issues = [
            issue
            for issue in safety_result["safety_issues"]
            if issue["severity"] in ["medium", "high"]
        ]
        if medium_issues:
            return True, safety_result

    elif safety_threshold == "low":
        # Low threshold: only block high severity issues (already handled by safe flag)
        pass

    return False, safety_result


if __name__ == "__main__":
    # Test with sample messages
    test_messages = [
        "This is a normal friendly message.",
        "I hate everything about this service!",
        "User John Doe lives at 123 Main St with phone 555-1234.",
    ]

    for msg in test_messages:
        result = check_message_safety(msg)
        print(f"Message: {msg[:50]}...")
        print(f"Safe: {result['safe']}")
        print(f"Issues: {len(result['safety_issues'])}")
        print()
