import os
import json
import sys
from azure.ai.contentsafety import (
    ContentSafetyClient,
)  # provider: Azure AI Content Safety (REST SDK)

from speech_client import get_client
from speech_models import SynthesisRequest, normalize_request

# Azure-specific environment variables
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
    raise RuntimeError(
        "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables"
    )

client = ContentSafetyClient(
    endpoint=AZURE_CONTENT_SAFETY_ENDPOINT, credential=AZURE_CONTENT_SAFETY_KEY
)


def detect_unsafe_content(script_text: str) -> dict:
    """Use Azure Content Safety API to check for unsafe content.

    Returns a JSON-like dict with categories, scores, and overall verdict.
    """
    result = client.analyze_content(text=script_text)
    # The SDK returns a `AnalyzeContentResult` object; we convert it to a simple dict
    return {
        "unsafe": result.unsafe,
        "categories": result.categories,
        "scores": result.scores,
        "suggested_action": result.suggested_action,
    }


def safe_for_synthesis(script_text: str) -> bool:
    """Simple wrapper that returns False when Azure Content Safety flags the text as unsafe."""
    report = detect_unsafe_content(script_text)
    # Example rule: block any content flagged as unsafe OR with high toxicity score
    if report["unsafe"]:
        return False
    # Optional additional checks (e.g., high toxicity) can be added here
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script_safety.py '<script text>'")
        sys.exit(1)
    script = sys.argv[1]
    report = detect_unsafe_content(script)
    print(json.dumps(report, indent=2))
    if safe_for_synthesis(script):
        print("Content is safe for synthesis.")
    else:
        print("Content flagged as unsafe; aborting synthesis.")
