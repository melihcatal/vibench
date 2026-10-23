import boto3
import os


def check_prompt_safety(payload, config=None):
    config = config or {}
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("comprehend", region_name=aws_region)

    text = payload["text"]

    # Detect dominant language first, as some Comprehend APIs require it
    detect_language_response = client.detect_dominant_language(Text=text)
    dominant_language_code = detect_language_response["Languages"][0]["LanguageCode"]

    # Detect sentiment and entities as indicators of safety/harmful content
    sentiment_response = client.detect_sentiment(Text=text, LanguageCode=dominant_language_code)
    entities_response = client.detect_entities(Text=text, LanguageCode=dominant_language_code)

    safety_concerns = []
    if sentiment_response["Sentiment"] in ["NEGATIVE", "MIXED"]:
        safety_concerns.append({"type": "sentiment", "level": sentiment_response["Sentiment"], "score": sentiment_response["SentimentScore"]})
    
    # Further analysis can be done based on detected entities for specific harmful content
    # For this example, we'll just return detected sentiment and entities

    return {
        "is_safe": not safety_concerns, # simplistic view, actual safety is more complex
        "concerns": safety_concerns,
        "sentiment": sentiment_response,
        "entities": entities_response,
    }
