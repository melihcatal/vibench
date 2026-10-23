from typing import Dict, List, Optional
from collections import defaultdict


def message_summary(processed_messages: List[Dict]) -> Dict:
    """
    Summarizes message processing results using Google Cloud's Natural Language API
    to analyze sentiment and entities in the messages.

    Args:
        processed_messages: List of dictionaries containing processed message data.

    Returns:
        Dict: Summary of message processing results, including counts and sentiment.
    """
    from google.cloud import language_v1

    client = language_v1.LanguageServiceClient()
    summary = {
        "total_messages": len(processed_messages),
        "sentiment_scores": [],
        "entities": defaultdict(int),
        "message_types": defaultdict(int),
    }

    for message in processed_messages:
        text = message.get("content", "")
        if not text:
            continue

        # Analyze sentiment
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
        summary["sentiment_scores"].append(sentiment.score)

        # Analyze entities
        entities = client.analyze_entities(request={"document": document}).entities
        for entity in entities:
            summary["entities"][entity.name] += 1

        # Count message types
        message_type = message.get("type", "unknown")
        summary["message_types"][message_type] += 1

    # Calculate average sentiment
    if summary["sentiment_scores"]:
        summary["average_sentiment"] = sum(summary["sentiment_scores"]) / len(
            summary["sentiment_scores"]
        )
    else:
        summary["average_sentiment"] = 0.0

    return summary
