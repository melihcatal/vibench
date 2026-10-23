import os
import boto3
from messaging_models import SafetyCheckResult


def check_message_safety(text_content: str) -> SafetyCheckResult:
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Using DetectSentiment as a proxy for content safety. In a real scenario,
    # one would use a more specific content moderation service or custom models.
    try:
        response = comprehend_client.detect_sentiment(
            Text=text_content, LanguageCode="en"
        )
        sentiment = response["Sentiment"]
        sentiment_score = response["SentimentScore"]

        is_safe = True
        details = f"Sentiment: {sentiment}, Scores: {sentiment_score}"

        # Example: if sentiment is 'NEGATIVE' or 'MIXED' with high confidence, consider it unsafe
        if sentiment in ["NEGATIVE", "MIXED"] and (
            sentiment_score.get("Negative", 0) > 0.8
            or sentiment_score.get("Mixed", 0) > 0.8
        ):
            is_safe = False
            details = "Potentially unsafe content detected based on sentiment."

        return SafetyCheckResult(is_safe=is_safe, details=details)
    except Exception as e:
        return SafetyCheckResult(
            is_safe=False, details=f"Error during sentiment detection: {str(e)}"
        )
