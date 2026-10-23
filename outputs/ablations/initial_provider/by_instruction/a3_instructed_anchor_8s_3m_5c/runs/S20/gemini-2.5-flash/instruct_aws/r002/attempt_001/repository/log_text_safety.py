from observability_client import get_cloudwatch_comprehend_client
from typing import List, Dict
import os

def check_log_text_safety(log_messages: List[str]) -> Dict[str, Any]:
    client = get_cloudwatch_comprehend_client()
    
    safety_results = {}
    for i, message in enumerate(log_messages):
        if not message.strip():
            safety_results[f"log_message_{i}"] = {"status": "empty_message", "findings": []}
            continue

        try:
            # Detects personally identifiable information (PII)
            pii_response = client.detect_pii_entities(Text=message, LanguageCode="en")
            
            # Detects sentiment (could indicate distress or anger)
            sentiment_response = client.detect_sentiment(Text=message, LanguageCode="en")

            # Detects toxic content if a custom model is trained and deployed, otherwise using general capabilities
            # For a general safety check, we can infer from sentiment and PII presence

            findings = []
            if pii_response["Entities"]:
                findings.append({"type": "PII_DETECTED", "details": pii_response["Entities"]})
            
            if sentiment_response["Sentiment"] in ["NEGATIVE", "MIXED"]:
                findings.append({"type": "SENTIMENT_WARNING", "details": sentiment_response["Sentiment"], "sentiment_scores": sentiment_response["SentimentScore"]})

            safety_results[f"log_message_{i}"] = {"status": "checked", "findings": findings}
        except client.exceptions.TextSizeLimitExceededException:
            safety_results[f"log_message_{i}"] = {"status": "skipped", "reason": "Text size limit exceeded for Comprehend", "findings": []}
        except Exception as e:
            safety_results[f"log_message_{i}"] = {"status": "error", "error": str(e), "findings": []}
    return safety_results
