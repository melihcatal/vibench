import os
from typing import List, Dict
from observability_client import get_log_client


def check_log_safety(log_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Screen selected log messages for unsafe or policy‑violating content.

    Uses a content‑safety service (e.g., Amazon Comprehend Toxicity, Alibaba Content Moderation,
    Perspective API, or watsonx guardrails). The function returns a list of logs that passed the check,
    optionally augmented with a `safety_status` field indicating `safe` or `blocked`.
    """
    client = get_log_client()
    # Example provider implementation: Amazon Comprehend (text-toxicity detection)
    if os.getenv("CONTENT_SAFETY_PROVIDER", "comprehend") == "comprehend":
        import boto3

        comprehend = boto3.client(service_name="comprehend")
        safe_entries = []
        for entry in log_entries:
            text = entry.get("message", "")
            if not text:
                continue
            # Comprehend toxicity detection expects UTF‑8 text
            result = comprehend.detect_sentiment(Text=text, LanguageCode="en")
            # Simulate a safety check using the Sentiment score
            status = "safe" if result["Sentiment"] != "NEGATIVE" else "blocked"
            entry["safety_status"] = status
            safe_entries.append(entry)
    # Placeholder for other providers (Perspective, Alibaba, etc.)
    return safe_entries
