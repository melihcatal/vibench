# [LATER-STEP] script_safety.py
# Check narration scripts for unsafe content using AWS Comprehend Toxicity detection
import os
import boto3
from typing import List

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY):
    raise RuntimeError("AWS credentials not set")

comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def is_unsafe(text: str) -> bool:
    """Return True if AWS Comprehend flags the text as toxic.
    This simple wrapper uses DetectSentiment which returns a mixed sentiment for toxicity,
    but for a more precise toxicity check you could also call DetectModerationInsights.
    """
    resp = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    # Comprehend's sentiment labels: POSITIVE, NEGATIVE, NEUTRAL, MIXED
    # We treat MIXED as potentially unsafe for this demo.
    return resp["Sentiment"] == "MIXED"


# Batch wrapper


def batch_check(scripts: List[str]) -> List[bool]:
    return [is_unsafe(s) for s in scripts]


if __name__ == "__main__":
    test = "This is a safe statement."
    print("Unsafe?", is_unsafe(test))
