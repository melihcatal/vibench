import os
from typing import List
from observability_client import get_logging_client
from google.cloud import language_v1


def check_log_text_safety(log_messages: List[str]) -> List[Dict[str, Any]]:
    """Check selected log message text for unsafe content using Google Cloud Natural Language API."""
    client = get_logging_client("google")
    language_client = language_v1.LanguageServiceClient()

    results = []
    for message in log_messages:
        document = language_v1.Document(
            content=message, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Analyze sentiment and content categories
        response = language_client.analyze_sentiment(request={"document": document})
        categories_response = language_client.classify_text(
            request={"document": document}
        )

        # Check for unsafe categories
        unsafe_categories = [
            category
            for category in categories_response.categories
            if category.confidence > 0.7
            and any(
                unsafe in category.name.lower()
                for unsafe in ["violence", "toxicity", "profanity", "identity"]
            )
        ]

        results.append(
            {
                "message": message,
                "is_safe": len(unsafe_categories) == 0,
                "sentiment_score": response.document_sentiment.score,
                "sentiment_magnitude": response.document_sentiment.magnitude,
                "unsafe_categories": [category.name for category in unsafe_categories],
            }
        )

    return results
