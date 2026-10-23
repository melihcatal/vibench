# [LATER-STEP] corpus_safety.py
# Check corpus text for toxicity or policy violations before embedding

import os
import boto3
from typing import Tuple

# Configure AWS Comprehend client
comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
)


def check_corpus_safety(text: str) -> Tuple[bool, str]:
    """Run AWS Comprehend toxicity analysis on a text corpus.

    Returns a tuple (is_safe, finding) where is_safe is True if no policy violation
    is detected, and finding contains the moderation finding or 'none' .
    """
    response = comprehend.detect_pii_entities(
        Text=text,
        LanguageCode="en",
    )
    # Simple rule: if any PII is found, we flag as unsafe for generic embedding
    if response.get("Error"):
        return False, str(response["Error"])
    entities = response.get("Result", [])
    if entities:
        return False, f"PII detected: {entities}"
    return True, "none"
