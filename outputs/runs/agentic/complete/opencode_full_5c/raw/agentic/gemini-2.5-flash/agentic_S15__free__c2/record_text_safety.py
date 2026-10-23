from database_client import get_comprehend_client
from typing import Dict, Any, List


def check_text_safety(text_content: str) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using AWS Comprehend.
    This includes detecting Personally Identifiable Information (PII) and sentiment analysis.

    Args:
        text_content: The text field of a document record to check.

    Returns:
        A dictionary containing detected PII entities and sentiment analysis results.
    """
    comprehend = get_comprehend_client()

    safety_results = {"pii_entities": [], "sentiment": "UNKNOWN", "sentiment_score": {}}

    if not text_content or not isinstance(text_content, str):
        return safety_results

    try:
        # Detect PII entities
        pii_response = comprehend.detect_pii_entities(
            Text=text_content, LanguageCode="en"
        )  # Assuming English for PII
        if pii_response and pii_response["Entities"]:
            safety_results["pii_entities"] = [
                {
                    "Type": entity["Type"],
                    "Score": entity["Score"],
                    "Text": text_content[entity["BeginOffset"] : entity["EndOffset"]],
                }
                for entity in pii_response["Entities"]
            ]

        # Detect sentiment
        sentiment_response = comprehend.detect_sentiment(
            Text=text_content, LanguageCode="en"
        )  # Assuming English for sentiment
        if sentiment_response:
            safety_results["sentiment"] = sentiment_response["Sentiment"]
            safety_results["sentiment_score"] = sentiment_response["SentimentScore"]

    except Exception as e:
        print(f"Error checking text safety with AWS Comprehend: {e}")

    return safety_results
