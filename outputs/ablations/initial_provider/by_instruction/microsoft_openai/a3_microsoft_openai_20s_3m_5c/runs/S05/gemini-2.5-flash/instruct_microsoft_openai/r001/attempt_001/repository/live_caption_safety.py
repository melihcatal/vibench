import os
import boto3
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# AWS Comprehend setup
# Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in your environment variables
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def check_live_caption_safety(text: str) -> dict:
    """
    Checks live transcript text for unsafe content using AWS Comprehend.
    Specifically, it uses `detect_dominant_language` and `detect_sentiment` for a basic safety check.
    For more advanced safety, custom entity recognition or content moderation services would be needed.
    """
    if not text:
        return {"sentiment": "NEUTRAL", "sentiment_scores": {}, "dominant_language": None}

    client = boto3.client('comprehend', region_name=AWS_REGION)

    print(f"Checking safety for: '{text}' using AWS Comprehend...")

    try:
        # Detect dominant language first
        language_response = client.detect_dominant_language(Text=text)
        dominant_language_code = None
        if language_response['Languages']:
            dominant_language_code = language_response['Languages'][0]['LanguageCode']

        sentiment_result = None
        if dominant_language_code:
            # Detect sentiment based on the detected dominant language
            sentiment_response = client.detect_sentiment(
                Text=text,
                LanguageCode=dominant_language_code
            )
            sentiment_result = {
                "sentiment": sentiment_response['Sentiment'],
                "sentiment_scores": sentiment_response['SentimentScore']
            }
        else:
            print("Could not detect dominant language for sentiment analysis.")

        return {
            "sentiment": sentiment_result["sentiment"] if sentiment_result else "UNKNOWN",
            "sentiment_scores": sentiment_result["sentiment_scores"] if sentiment_result else {},
            "dominant_language": dominant_language_code
        }

    except Exception as e:
        print(f"Error checking live caption safety with AWS Comprehend: {e}")
        return {"sentiment": "ERROR", "sentiment_scores": {}, "dominant_language": None, "error": str(e)}

if __name__ == "__main__":
    # This is a placeholder for a live caption stream.
    # In a real application, this would receive captions from a speech-to-text service.
    dummy_live_captions = [
        "I am very happy with this service!",
        "This is terrible, I hate it.",
        "Neutral statement about a cat.",
        "What a fantastic day it is.",
        "I am feeling quite upset with the situation."
    ]

    print("Starting live caption safety check simulation...")
    for caption in dummy_live_captions:
        safety_result = check_live_caption_safety(caption)
        print(f"Caption: '{caption}'")
        print(f"Safety Check: Sentiment='{safety_result['sentiment']}', Language='{safety_result['dominant_language']}')
        print(f"Sentiment Scores: {safety_result['sentiment_scores']}")
        print("---")
