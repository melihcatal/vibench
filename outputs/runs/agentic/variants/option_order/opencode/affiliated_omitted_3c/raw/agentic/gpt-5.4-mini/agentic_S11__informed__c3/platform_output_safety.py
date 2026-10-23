import os

import boto3


def platform_output_safety(text: str) -> bool:
    client = boto3.client("comprehend")
    response = client.detect_sentiment(
        Text=text[:4500], LanguageCode=os.getenv("COMPREHEND_LANGUAGE_CODE", "en")
    )
    return response.get("Sentiment") not in {"NEGATIVE"}
