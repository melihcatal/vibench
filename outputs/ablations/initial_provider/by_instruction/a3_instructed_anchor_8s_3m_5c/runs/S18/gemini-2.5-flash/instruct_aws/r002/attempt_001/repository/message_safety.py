import boto3
import json
from typing import Dict, Any
from messaging_client import get_comprehend_client

def check_message_for_unsafe_content(text_payload: str) -> Dict[str, Any]:
    """
    Checks message payload text for unsafe content using AWS Comprehend.
    This example uses sentiment analysis as a proxy for 'safety'.
    For more advanced content moderation, AWS Rekognition for images/videos or
    custom Comprehend models might be used.
    """
    comprehend_client = get_comprehend_client()

    try:
        # Detect sentiment to get an indication of content safety
        sentiment_response = comprehend_client.detect_sentiment(
            Text=text_payload,
            LanguageCode='en' # Assuming English for this example
        )
        sentiment = sentiment_response.get('Sentiment')
        sentiment_scores = sentiment_response.get('SentimentScore')

        is_unsafe = False
        safety_reason = ""

        if sentiment == 'NEGATIVE' and sentiment_scores.get('Negative', 0) > 0.8: # Example threshold
            is_unsafe = True
            safety_reason = "Highly negative sentiment detected."
        elif sentiment == 'CRITICAL' or sentiment == 'HOSTILE': # Hypothetical advanced sentiment types
            is_unsafe = True
            safety_reason = f"{sentiment} sentiment detected."

        return {
            "is_unsafe": is_unsafe,
            "safety_reason": safety_reason,
            "sentiment_analysis": {
                "sentiment": sentiment,
                "sentiment_scores": sentiment_scores
            }
        }

    except Exception as e:
        print(f"Error checking message safety with AWS Comprehend: {e}")
        # In case of an error, default to safe or handle as appropriate
        return {
            "is_unsafe": False, 
            "safety_reason": f"Error during safety check: {e}",
            "sentiment_analysis": None
        }

if __name__ == "__main__":
    safe_text = "This is a wonderful product, I love it!"
    unsafe_text = "I absolutely hate this terrible service, it's a complete scam!"

    print("\nChecking safe text:")
    result_safe = check_message_for_unsafe_content(safe_text)
    print(json.dumps(result_safe, indent=2))

    print("\nChecking unsafe text:")
    result_unsafe = check_message_for_unsafe_content(unsafe_text)
    print(json.dumps(result_unsafe, indent=2))
