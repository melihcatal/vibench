import os
import boto3
from typing import List, Dict


def moderate_text_for_pii(text: str, language_code: str = "en") -> List[Dict]:
    # AWS Comprehend client
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in environment variables
    # or configured via AWS CLI/SDK default profiles.
    comprehend = boto3.client(
        "comprehend",
        region_name=os.environ.get(
            "AWS_REGION", "us-east-1"
        ),  # AWS_REGION is provider-specific
    )

    try:
        # Detect PII entities in the text
        response = comprehend.detect_pii_entities(Text=text, LanguageCode=language_code)
        return response["Entities"]
    except Exception as e:
        raise Exception(f"Failed to moderate text for PII using AWS Comprehend: {e}")


def moderate_text_for_sentiment(text: str, language_code: str = "en") -> Dict:
    # AWS Comprehend client
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in environment variables
    # or configured via AWS CLI/SDK default profiles.
    comprehend = boto3.client(
        "comprehend",
        region_name=os.environ.get(
            "AWS_REGION", "us-east-1"
        ),  # AWS_REGION is provider-specific
    )

    try:
        # Detect sentiment in the text
        response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
        return {
            "Sentiment": response["Sentiment"],
            "SentimentScore": response["SentimentScore"],
        }
    except Exception as e:
        raise Exception(f"Failed to detect sentiment using AWS Comprehend: {e}")


if __name__ == "__main__":
    example_claim = "This user frequently complains about slow logins and requests a password reset. Their email is test@example.com."
    try:
        pii_entities = moderate_text_for_pii(example_claim)
        print(f"Detected PII entities: {pii_entities}")

        sentiment = moderate_text_for_sentiment(example_claim)
        print(f"Detected sentiment: {sentiment}")

    except Exception as e:
        print(f"Error: {e}")
