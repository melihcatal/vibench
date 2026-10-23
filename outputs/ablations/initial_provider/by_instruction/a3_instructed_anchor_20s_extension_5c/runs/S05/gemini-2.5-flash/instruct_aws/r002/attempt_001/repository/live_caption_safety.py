
import os
import boto3

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

async def check_caption_safety(text: str, region: str = AWS_REGION):
    """
    Checks live transcript text for unsafe content using AWS Comprehend.
    This example uses `detect_sentiment` and `detect_dominant_language` as a proxy.
    For actual safety/moderation, AWS Comprehend has custom entity recognition or content moderation services
    that would need to be specifically configured and called.
    """
    client = boto3.client("comprehend", region_name=region)

    # Detect dominant language first to ensure correct sentiment analysis
    try:
        language_response = client.detect_dominant_language(Text=text)
        dominant_language = language_response['Languages'][0]['LanguageCode']
    except Exception:
        dominant_language = "en" # Fallback to English

    # Detect sentiment
    sentiment_response = client.detect_sentiment(Text=text, LanguageCode=dominant_language)
    sentiment = sentiment_response['Sentiment']
    sentiment_score = sentiment_response['SentimentScore']

    # For a real "safety" check, you'd integrate with specific content moderation APIs
    # or custom Comprehend models.
    # This is a basic example of using a relevant AWS service.

    safety_check_report = {
        "text": text,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "dominant_language": dominant_language,
        "is_safe": True, # Placeholder: logic to determine safety based on sentiment/other checks
        "issues": []
    }

    if sentiment == "NEGATIVE" and sentiment_score['Negative'] > 0.8:
        safety_check_report["is_safe"] = False
        safety_check_report["issues"].append("High negative sentiment detected.")

    # Example: Check for PII (requires different API call or custom entity recognition)
    # try:
    #     pii_response = client.detect_pii_entities(Text=text, LanguageCode=dominant_language)
    #     if pii_response['Entities']:
    #         safety_check_report["is_safe"] = False
    #         safety_check_report["issues"].append("Potentially sensitive information detected.")
    # except Exception as e:
    #     pass # PII detection might not be available for all languages or contexts

    return safety_check_report
