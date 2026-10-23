from observability_client import get_datadog_headers
import requests
from observability_models import TextSafetyReport

import os


def check_metric_annotation_safety(annotation: str) -> TextSafetyReport:
    """
    Run an LLM moderation step to ensure `annotation` is safe.
    Uses Amazon Comprehend Toxicity (Boto3) as the concrete provider.
    Returns a `TextSafetyReport` with a boolean `safe` flag and optionally flagged tokens.
    """
    client = boto3.client(
        "comprehend",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    result = client.detect_toxic_content(Text=annotation)
    safe = result.get("ToxicContentClassification") == "NONE"
    flagged = result.get("DetectedLanguages", [])
    return {
        "safe": safe,
        "flagged_tokens": flagged,
    }
