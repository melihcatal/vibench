from security_client import SecurityClient
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    client = SecurityClient()
    # Using DetectSentiment as an example for content analysis.
    # For actual toxicity, Comprehend's content moderation or custom classification would be more appropriate
    # or Bedrock Guardrails. For this example, we'll use detect_sentiment as a placeholder for content analysis.
    response = client.comprehend_client.detect_sentiment(
        Text=request.text, LanguageCode="en"
    )

    unsafe_categories = []
    # This is a simplified example. A real safety check would involve more sophisticated analysis
    # and potentially other Comprehend APIs like detect_moderation_labels or custom classification.
    if (
        response["Sentiment"] == "NEGATIVE"
        and response["SentimentScore"]["Negative"] > 0.8
    ):
        unsafe_categories.append("HIGHLY_NEGATIVE_SENTIMENT")

    return PayloadSafetyResponse(unsafe_categories=unsafe_categories)
