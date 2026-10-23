from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from typing import Dict, Any, List
import os

# Initialize Azure Text Analytics client for content moderation
text_analytics_client = TextAnalyticsClient(
    endpoint=os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_TEXT_ANALYTICS_KEY")),
)


def profile_moderation(text: str, language: str = "en") -> Dict[str, Any]:
    """
    Moderates profile text before account activation using Azure Content Moderator.

    Args:
        text: Profile text to moderate
        language: Language code for moderation (default: 'en')

    Returns:
        Dictionary containing moderation results and flags
    """
    if not text:
        return {
            "moderation_passed": True,
            "provider": "azure_content_moderator",
            "flags": [],
        }

    documents = [{"id": "1", "text": text, "language": language}]

    # Analyze for profanity
    profanity_result = text_analytics_client.recognize_profanity(documents=documents)

    # Analyze for PII
    pii_result = text_analytics_client.recognize_pii_entities(documents=documents)

    # Analyze sentiment and key phrases
    sentiment_result = text_analytics_client.analyze_sentiment(documents=documents)

    # Compile results
    flags = []
    moderation_passed = True

    for doc in profanity_result:
        if doc.is_error:
            continue
        for match in doc.profanity.matches:
            flags.append(
                {
                    "category": "profanity",
                    "severity": match.severity,
                    "text": match.term,
                    "offset": match.offset,
                    "length": match.length,
                }
            )
            moderation_passed = False

    for doc in pii_result:
        if doc.is_error:
            continue
        for entity in doc.entities:
            flags.append(
                {
                    "category": "pii",
                    "subcategory": entity.category,
                    "text": entity.text,
                    "offset": entity.offset,
                    "length": entity.length,
                    "confidence_score": entity.confidence_score,
                }
            )
            moderation_passed = False

    for doc in sentiment_result:
        if doc.is_error:
            continue
        if doc.sentiment == "negative":
            flags.append(
                {
                    "category": "sentiment",
                    "severity": "high",
                    "text": text,
                    "sentiment_score": {
                        "positive": doc.confidence_scores.positive,
                        "neutral": doc.confidence_scores.neutral,
                        "negative": doc.confidence_scores.negative,
                    },
                }
            )
            moderation_passed = False

    return {
        "moderation_passed": moderation_passed,
        "flags": flags,
        "provider": "azure_content_moderator",
        "model": "text-analytics-v3.1",
    }
