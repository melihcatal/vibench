"""
Moderate a batch of user messages and return per-message decisions
using Azure AI Content Safety.
"""

from typing import Any, Dict, List, Optional

from safety_client import (
    get_azure_content_safety_config,
    get_analyze_batch_url,
    create_azure_content_safety_session,
    build_batch_moderation_payload,
)
from safety_models import (
    ModerationResponse,
    BatchModerationResult,
    BatchModerationResponse,
    parse_azure_analyze_response,
)


def moderate_batch(
    texts: List[str],
    config: Optional[Dict[str, str]] = None,
) -> BatchModerationResponse:
    """
    Send a batch of *texts* to Azure AI Content Safety
    (/contentsafety/text:analyzeBatch) and return per-message decisions.

    Provider: Azure AI Content Safety
    Endpoint: {azure_endpoint}/contentsafety/text:analyzeBatch?api-version=2024-02-15-preview
    """
    cfg = config or get_azure_content_safety_config()
    session, cfg = create_azure_content_safety_session(cfg)
    url = get_analyze_batch_url(cfg)

    payload = build_batch_moderation_payload(texts)
    resp = session.post(url, json=payload)
    resp.raise_for_status()
    raw = resp.json()

    results: List[BatchModerationResult] = []
    # Azure batch response includes "result" with list of "index" and "analysis"
    batch_items = raw.get("result", [])

    for item in batch_items:
        idx = item.get("index", 0)
        analysis = item.get("analysis", {})
        text = texts[idx]
        moderation = parse_azure_analyze_response(text, analysis)
        results.append(
            BatchModerationResult(
                index=idx,
                text=text,
                moderation=moderation,
            )
        )

    return BatchModerationResponse(results=results)


def moderate_batch_raw(
    texts: List[str], config: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Return the raw Azure AI Content Safety batch JSON response."""
    cfg = config or get_azure_content_safety_config()
    session, cfg = create_azure_content_safety_session(cfg)
    url = get_analyze_batch_url(cfg)
    payload = build_batch_moderation_payload(texts)
    resp = session.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    messages = [
        "Hello, how are you?",
        "I want to hurt someone.",
        "Have a great day!",
    ]
    resp = moderate_batch(messages)
    for r in resp.results:
        print(f"[{r.index}] safe={r.moderation.is_safe}  text={r.text!r}")
