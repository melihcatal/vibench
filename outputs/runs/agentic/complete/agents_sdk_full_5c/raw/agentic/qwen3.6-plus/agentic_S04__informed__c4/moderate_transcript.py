"""Moderate transcript text before publishing using Azure AI Content Safety.

Uses Azure AI Content Safety REST API for text content moderation analysis.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY environment variables.
"""

import os
from typing import List, Optional, Dict
import requests


AZURE_CONTENT_SAFETY_VERSION = "2024-02-15-preview"


def get_azure_content_safety_config() -> dict:
    """Retrieve Azure Content Safety endpoint and key from environment."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables are required"
        )
    return {"endpoint": endpoint, "key": key}


def moderate_text(
    text: str,
    output_type: str = "EightSeverityLevels",
) -> Dict:
    """Send text to Azure AI Content Safety for moderation analysis.

    Analyzes text for hate, self-harm, sexual, and violence categories.

    Args:
        text: The text to moderate.
        output_type: 'FourSeverityLevels' or 'EightSeverityLevels'.

    Returns:
        Dict with moderation results from Azure Content Safety.
    """
    config = get_azure_content_safety_config()

    url = f"{config['endpoint']}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": config["key"],
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "outputType": output_type,
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def moderate_transcript_segments(
    segments: List[str],
    threshold: int = 4,
) -> List[dict]:
    """Moderate a list of transcript segments using Azure AI Content Safety.

    Args:
        segments: List of text segments to check.
        threshold: Severity threshold (0-8) for flagging content.

    Returns:
        List of dicts with moderation results per segment.
    """
    results = []
    categories = ["hate", "selfHarm", "sexual", "violence"]

    for i, text in enumerate(segments):
        moderation = moderate_text(text)

        flagged_categories = []
        for cat in categories:
            severity = moderation.get(f"{cat}Result", {}).get("severity", 0)
            flagged_categories.append({
                "category": cat,
                "severity": severity,
                "flagged": severity >= threshold,
            })

        any_flagged = any(fc["flagged"] for fc in flagged_categories)

        results.append({
            "index": i,
            "text": text,
            "safe": not any_flagged,
            "categories": flagged_categories,
        })

    return results


def main():
    import json
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            data = json.load(f)
        segments = data if isinstance(data, list) else data.get("segments", [])
    else:
        segments = [
            "This is a safe and friendly meeting summary.",
            "The team discussed project milestones.",
        ]

    results = moderate_transcript_segments(segments)
    for r in results:
        status = "SAFE" if r["safe"] else "FLAGGED"
        print(f"[{r['index']}] {status}: {r['text'][:80]}")


if __name__ == "__main__":
    main()
