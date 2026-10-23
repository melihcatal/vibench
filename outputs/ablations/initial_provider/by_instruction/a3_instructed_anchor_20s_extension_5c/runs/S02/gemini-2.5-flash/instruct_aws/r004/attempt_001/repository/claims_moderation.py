import os
import boto3
import json
from typing import List, Dict, Any

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

def moderate_text_with_comprehend(text: str) -> Dict[str, Any]:
    """
    Moderates free-text claims or notes using AWS Comprehend.
    This example demonstrates sentiment analysis and detect PII.
    For full content moderation, custom classification models might be needed.
    """
    client = boto3.client("comprehend", region_name=AWS_REGION)

    try:
        sentiment_response = client.detect_sentiment(Text=text, LanguageCode="en")
        pii_response = client.detect_pii_entities(Text=text, LanguageCode="en")

        moderation_results = {
            "sentiment": sentiment_response.get("Sentiment"),
            "sentiment_score": sentiment_response.get("SentimentScore"),
            "pii_entities": [
                {"type": entity.get("Type"), "score": entity.get("Score"), "text": text[entity.get("BeginOffset"):entity.get("EndOffset")]}
                for entity in pii_response.get("Entities", [])
            ],
            "moderation_flags": []
        }
        
        # Example of simple flagging based on sentiment or PII detection
        if moderation_results["sentiment"] == "NEGATIVE":
            moderation_results["moderation_flags"].append("Negative Sentiment Detected")
        if moderation_results["pii_entities"]:
            moderation_results["moderation_flags"].append("Potential PII Detected")

        return moderation_results

    except client.exceptions.InvalidRequestException as e:
        print(f"Invalid request for Comprehend: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error moderating text with Comprehend: {e}")
        raise

if __name__ == "__main__":
    example_claim = "This is a great experience, but I also want to add my phone number 123-456-7890 and email test@example.com."
    # example_claim = "I am very unhappy with this service."

    try:
        moderation_output = moderate_text_with_comprehend(example_claim)
        print("Moderation Results:")
        print(json.dumps(moderation_output, indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")
