import os
from content_safety_client import (
    ContentSafetyClient,
)  # placeholder for real provider client


def check_corpus_safety(texts: list[str]) -> dict:
    """Run a content safety check on each supplied corpus text.

    Returns a dict mapping each text to a safety verdict ('safe' or 'unsafe')
    and optionally a reason for unsafe classification.
    Uses the Perspective API (via requests SDK) as the concrete provider.
    """
    client = ContentSafetyClient()
    client.set_provider("perspective")
    verdicts = {}
    for t in texts:
        resp = client.analyze_toxicity(text=t)
        # Assume resp is a JSON with fields: 'attributeScores' -> 'SEVERE_TOXICITY' -> 'summaryScore' -> 'value'
        score = (
            resp.get("attributeScores", {})
            .get("SEVERE_TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0.0)
        )
        verdict = "safe" if score < 0.5 else "unsafe"
        verdicts[t] = {
            "verdict": verdict,
            "reason": f"Score={score}" if verdict == "unsafe" else None,
        }
    return verdicts
