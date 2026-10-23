# LATER-STEP
# record_text_safety.py - Check user-generated document fields for unsafe content

# Provider: Amazon Comprehend Toxicity (managed text content safety)
import boto3
import json
from database_models import DocumentResponse

comprehend = boto3.client(
    "comprehend",
    region_name="us-east-1",
    # AWS credentials are taken from environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
)


def is_text_safe(text: str) -> bool:
    """Use Amazon Comprehend to detect toxic content in a string.

    Args:
        text (str): The text to evaluate.

    Returns:
        bool: True if the text is judged safe, False otherwise.
    """
    response = comprehend.detect_pii_entities(Text=text, LanguageCode="en")
    # Simple heuristic: if any PII is found, treat as unsafe for generic storage
    return len(response.get("Entities", [])) == 0
