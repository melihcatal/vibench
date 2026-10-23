import os
import boto3

def check_message_safety(text: str, language_code: str = "en") -> dict:
    """
    Checks message payload text for unsafe content using AWS Comprehend
    for PII detection and sentiment analysis.
    """
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    safety_findings = {}
    try:
        # PII Detection
        pii_response = comprehend_client.detect_pii_entities(
            Text=text,
            LanguageCode=language_code
        )
        pii_entities = [
            {"Type": entity["Type"], "Text": text[entity["BeginOffset"]:entity["EndOffset"]]}
            for entity in pii_response.get("Entities", [])
        ]
        safety_findings["pii_detected"] = len(pii_entities) > 0
        safety_findings["pii_entities"] = pii_entities

        # Sentiment Analysis (can indicate potentially unsafe/negative tone)
        sentiment_response = comprehend_client.detect_sentiment(
            Text=text,
            LanguageCode=language_code
        )
        safety_findings["sentiment"] = sentiment_response["Sentiment"]
        safety_findings["sentiment_scores"] = sentiment_response["SentimentScore"]

        return {"status": "success", "findings": safety_findings}
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    # Example Usage (requires AWS_REGION environment variable)
    # Ensure AWS credentials are configured
    # sensitive_text = "Please send my order to 123 Main St. My email is john.doe@example.com."
    # safety_report = check_message_safety(sensitive_text)
    # print(f"Message Safety Report: {safety_report}")
    #
    # neutral_text = "This is a normal message."
    # safety_report_neutral = check_message_safety(neutral_text)
    # print(f"Neutral Message Safety Report: {safety_report_neutral}")
    pass
