# Check free‑text metric labels or annotations for unsafe text using OpenAI Moderation (GPT).

import os
from .observability_client import init_client
from .observability_models import normalize_datadog_points

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

import openai

openai.api_key = OPENAI_API_KEY

METRIC = "system.cpu.load"
# Assume we have a label such as "hostname:prod" and annotation "contains sensitive user data"
LABEL = "hostname:prod"
ANNOTATION = "contains sensitive user data"

UNSAFE_PHRASES = [
    "password",
    "secret",
    "key",
    "credential",
    "private",
    "confidential",
]


def unsafe_check(text: str) -> bool:
    """Call OpenAI moderation endpoint to detect unsafe content."""
    response = openai.Moderation.create(input=text)
    flagged = response["results"][0]["flagged"]
    return flagged


def metric_annotation_safety():
    """Check both LABEL and ANNOTATION for unsafe text and return a safety flag."""
    unsafe = unsafe_check(LABEL) or unsafe_check(ANNOTATION)
    return {
        "metric": METRIC,
        "label": LABEL,
        "annotation": ANNOTATION,
        "safe": not unsafe,
        "details": {
            "label_flagged": unsafe_check(LABEL),
            "annotation_flagged": unsafe_check(ANNOTATION),
        },
    }


if __name__ == "__main__":
    safety = metric_annotation_safety()
    print(safety)

# ---------------------------------------------------------------------------
# Run with: python metric_annotation_safety.py
# ---------------------------------------------------------------------------
