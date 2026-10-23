"""
Moderate user text for unsafe or policy-violating content
using Azure AI Content Safety.
"""

from typing import Any, Dict, Optional

from safety_client import (
    get_azure_content_safety_config,
    get_analyze_text_url,
    create_azure_content_safety_session,
    build_moderation_payload,
)
from safety_models import (
    ModerationResponse,
    parse_azure_analyze_response,
)


def moderate_text(
    text: str,
    config: Optional[Dict[str, str]] = None,
) -> ModerationResponse:
    """
    Send *text* to Azure AI Content Safety (/contentsafety/text:analyze)
    and return a normalised ModerationResponse.

    Provider: Azure AI Content Safety
    Endpoint: {azure_endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview
    """
    cfg = config or get_azure_content_safety_config()
    session, cfg = create_azure_content_safety_session(cfg)
    url = get_analyze_text_url(cfg)

    payload = build_moderation_payload(text)
    resp = session.post(url, json=payload)
    resp.raise_for_status()
    raw = resp.json()

    return parse_azure_analyze_response(text, raw)


def moderate_text_raw(text: str, config: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Return the raw Azure AI Content Safety JSON response for debugging."""
    cfg = config or get_azure_content_safety_config()
    session, cfg = create_azure_content_safety_session(cfg)
    url = get_analyze_text_url(cfg)
    payload = build_moderation_payload(text)
    resp = session.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "This is a harmless message."
    result = moderate_text(sample)
    print(f"Safe: {result.is_safe}")
    for c in result.categories:
        print(f"  {c.category}: severity={c.severity}, flagged={c.is_flagged}")
