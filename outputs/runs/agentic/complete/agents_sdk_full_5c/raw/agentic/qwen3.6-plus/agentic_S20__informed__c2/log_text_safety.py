"""
log_text_safety.py

Check selected log message text for unsafe content using the
Perspective API (Google Jigsaw) via REST requests.

Required env: PERSPECTIVE_API_KEY
"""

import os
import requests
from typing import List, Dict, Any
from observability_models import QueryResponse, LogQueryResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_log_safety(
    log_results: QueryResponse,
    attributes: List[str] | None = None,
    threshold: float = 0.7,
) -> List[Dict[str, Any]]:
    """
    Analyze log messages for toxic or unsafe content using the
    Perspective API.

    Args:
        log_results: QueryResponse with log entries to check.
        attributes: Perspective attributes to evaluate
                    (default: TOXICITY, SEVERE_TOXICITY, THREAT).
        threshold: Score above which a message is flagged.

    Returns:
        List of dicts with message text, attribute scores, and flag status.
    """
    if attributes is None:
        attributes = ["TOXICITY", "SEVERE_TOXICITY", "THREAT"]

    api_key = os.environ["PERSPECTIVE_API_KEY"]
    results = []

    messages = [r.message for r in log_results.results if r.message and len(r.message) > 0]
    # Deduplicate
    seen = set()
    unique_messages = []
    for m in messages:
        if m not in seen:
            seen.add(m)
            unique_messages.append(m)

    for message in unique_messages:
        payload = {
            "comment": {"text": message},
            "requestedAttributes": {attr: {} for attr in attributes},
            "languages": ["en"],
        }

        resp = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json=payload,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        scores = {}
        flagged = False
        for attr in attributes:
            attr_data = data.get("attributeScores", {}).get(attr, {})
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            scores[attr] = round(score, 4)
            if score >= threshold:
                flagged = True

        results.append({
            "message": message,
            "scores": scores,
            "flagged": flagged,
        })

    return results


def filter_flagged_messages(
    safety_results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Return only the entries that were flagged as unsafe."""
    return [r for r in safety_results if r["flagged"]]


if __name__ == "__main__":
    from query_error_logs import query_error_logs

    lg = os.environ.get("CLOUDWATCH_LOG_GROUP", "/app/production")
    errors = query_error_logs(
        log_group_name=lg,
        hours_back=4,
        log_level_filter="ERROR",
        limit=20,
    )
    safety = check_log_safety(errors, threshold=0.5)
    flagged = filter_flagged_messages(safety)
    print(f"Checked {len(safety)} messages, {len(flagged)} flagged.")
    for item in flagged:
        print(f"  FLAGGED: {item['message'][:80]}  scores={item['scores']}")
