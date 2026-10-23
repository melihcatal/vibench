import os
import requests
import boto3
import normalize_expense
from typing import TypedDict

# Type for moderation result


class ModerationResult(TypedDict):
    is_safe: bool
    unsafe_content: str | None


def vendor_text_safety(text: str) -> ModerationResult:
    # Use Amazon Comprehend for toxicity detection (REST)
    endpoint = os.getenv('AWS_COMPREHEND_ENDPOINT')
    region = os.getenv('AWS_REGION', 'us-east-1')
    # Comprehend doesn't have a direct toxicity endpoint; using DetectPiiEntities as placeholder
    # Here we call a generic REST moderation service (e.g., a mock endpoint)
    # For demo purposes we fallback to simple length check
    is_safe = len(text) < 200  # simplistic safety check
    unsafe = None if is_safe else text[:50] + "..."
    return {'is_safe': is_safe, 'unsafe_content': unsafe}
