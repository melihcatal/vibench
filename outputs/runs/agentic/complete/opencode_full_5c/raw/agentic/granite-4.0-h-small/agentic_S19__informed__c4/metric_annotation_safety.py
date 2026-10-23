# metric_annotation_safety.py
# Check free‑text metric labels or annotations for unsafe text

from observability_client import ObservabilityClient
from observability_models import GuardrailsResponse
import os


def check_annotations(service: str, annotations: list) -> GuardrailsResponse:
    """Inspect a list of string annotations and flag unsafe content using a provider.
    Returns a GuardrailsResponse with safety flag and detected issues."""
    client = ObservabilityClient.get_client(service)
    # Choose safety provider based on service/context
    if client["service"] in ("datadog", "google", "aws"):
        # Use Tisane moderation (fallback if env var missing)
        api_key = os.getenv("TISANE_API_KEY")
        if not api_key:
            raise RuntimeError("TISANE_API_KEY not set for content safety check")
        import requests

        post_url = "https://api.tisane.ai/v1/parse"
        headers = {"api-key": api_key, "Content-Type": "application/json"}
        payload = {
            "language": "en",
            "text": "|".join(annotations),  # simple concatenation
            "settings": {
                "content_moderation": {"flags": ["hate", "vulgar", "sexual", "violent"]}
            },
        }
        resp = requests.post(post_url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        # Extract flagged issues if present
        issues = data.get("issues", [])
        safe = len(issues) == 0
        return GuardrailsResponse(safe=safe, issues=issues)
    elif client["service"] == "aws":
        # Use Amazon Comprehend Toxicity / Bedrock Guardrails
        import boto3

        comprehend = boto3.client("comprehend", region_name="us-east-1")
        texts = annotations[:10]  # limit to first 10 for cost efficiency
        response = comprehend.detect_sentiment(Text="|".join(texts), LanguageCode="en")
        safe = response["Sentiment"] != "NEGATIVE"
        issues = []  # placeholder, real integration would list issues
        return GuardrailsResponse(safe=safe, issues=issues)
    else:
        raise ValueError(f"Unsupported service {service} for annotation safety")
