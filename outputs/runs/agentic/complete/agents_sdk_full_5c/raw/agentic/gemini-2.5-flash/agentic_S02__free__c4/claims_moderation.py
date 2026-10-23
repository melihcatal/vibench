import os
import boto3
from typing import Dict, Any

# AWS Comprehend
# Ensure AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) are set in environment variables or AWS config.

def moderate_text_claim(text_claim: str) -> Dict[str, Any]:
    """Moderates a free-text claim using AWS Comprehend for sentiment and PII detection."""
    # AWS SDK Boto3 will automatically pick up credentials from environment variables or IAM roles
    comprehend = boto3.client('comprehend', region_name=os.environ.get("AWS_REGION", "us-east-1"))

    results = {
        "text": text_claim,
        "sentiment": None,
        "sentiment_score": None,
        "languages": [],
        "pii_entities": []
    }

    if not text_claim.strip():
        results["message"] = "Empty text claim provided for moderation."
        return results

    try:
        # Detect dominant language first
        language_response = comprehend.detect_dominant_language(Text=text_claim)
        if language_response["Languages"]:
            dominant_language = language_response["Languages"][0]["LanguageCode"]
            results["languages"] = [lang["LanguageCode"] for lang in language_response["Languages"]]
        else:
            dominant_language = "en" # Default to English if language detection fails
            results["message"] = "Could not detect dominant language, defaulting to English."
        
        # Analyze sentiment
        sentiment_response = comprehend.detect_sentiment(Text=text_claim, LanguageCode=dominant_language)
        results["sentiment"] = sentiment_response["Sentiment"]
        results["sentiment_score"] = sentiment_response["SentimentScore"]

        # Detect PII entities (e.g., credit card numbers, email addresses, names)
        pii_response = comprehend.detect_pii_entities(Text=text_claim, LanguageCode=dominant_language)
        for entity in pii_response["Entities"]:
            results["pii_entities"].append({
                "type": entity["Type"],
                "score": entity["Score"],
                "text": text_claim[entity["BeginOffset"]:entity["EndOffset"]]
            })

    except comprehend.exceptions.InvalidRequestException as e:
        results["error"] = f"Invalid request for Comprehend: {e}"
    except comprehend.exceptions.TextSizeLimitExceededException as e:
        results["error"] = f"Text size limit exceeded for Comprehend: {e}"
    except Exception as e:
        results["error"] = f"An unexpected AWS Comprehend error occurred: {e}"

    return results

if __name__ == "__main__":
    # Example free-text claims or notes
    claim_positive = "The user provided excellent feedback and was very satisfied with the login experience. No issues."
    claim_negative = "There was a critical error during login, and the user's private email address test@example.com was exposed accidentally. User was very angry."
    claim_neutral = "User logged in from a new device at 10:30 AM."
    claim_empty = ""

    print("\n--- Moderating Positive Claim ---")
    print(moderate_text_claim(claim_positive))

    print("\n--- Moderating Negative Claim ---")
    print(moderate_text_claim(claim_negative))

    print("\n--- Moderating Neutral Claim ---")
    print(moderate_text_claim(claim_neutral))

    print("\n--- Moderating Empty Claim ---")
    print(moderate_text_claim(claim_empty))

    # Check for AWS credentials warning
    if not os.environ.get("AWS_ACCESS_KEY_ID") or not os.environ.get("AWS_SECRET_ACCESS_KEY") or not os.environ.get("AWS_REGION"):
        print("\nWARNING: AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) "
              "are not set in environment variables. AWS Comprehend calls may fail without authentication.")
        print("Please set them up or configure your AWS CLI before running this example.")
