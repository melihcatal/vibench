"""
[LATER-STEP] Moderate free-text claims or notes using Anthropic Messages API.

Uses the Anthropic Messages API (sdk=anthropic, model=claude-sonnet-4-20250514)
to evaluate federated login audit event notes and free-text claims for safety,
toxicity, PII exposure, and policy violations.

Required env vars: ANTHROPIC_API_KEY
"""

import logging
from typing import Any, Dict, List, Optional

import anthropic

from identity_client import get_audit_logger
from identity_models import AuditEvent

logger = logging.getLogger(__name__)

# Anthropic Claude model family identifier
MODERATION_MODEL = "claude-sonnet-4-20250514"


def moderate_text(
    text: str,
    api_key: Optional[str] = None,
    model: str = MODERATION_MODEL,
) -> Dict[str, Any]:
    """
    Moderate free-text content using Anthropic Claude via the Messages API.

    Anthropic Messages API endpoint:
        POST https://api.anthropic.com/v1/messages

    Required env var: ANTHROPIC_API_KEY
    """
    if not text or not text.strip():
        return {
            "text": text,
            "flagged": False,
            "categories": {},
            "risk_level": "none",
            "explanation": "Empty text, no moderation needed.",
        }

    system_prompt = (
        "You are a content moderation system for identity and access management audit logs. "
        "Analyze the provided text for: "
        "1. Toxicity or harassment language "
        "2. Exposed PII (passwords, SSNs, credit card numbers, API keys) "
        "3. Injection attempts (SQL, XSS, command injection patterns) "
        "4. Policy violations (unauthorized access descriptions, credential sharing) "
        "5. Suspicious activity descriptions "
        ""
        "Respond with a JSON object containing: "
        "- 'flagged': boolean, true if any concerns found "
        "- 'categories': object with boolean flags for each concern type above "
        "- 'risk_level': one of 'none', 'low', 'medium', 'high', 'critical' "
        "- 'explanation': brief explanation of findings "
        "- 'redacted_text': text with any exposed sensitive values replaced with [REDACTED] "
        ""
        "Respond ONLY with valid JSON, no markdown formatting."
    )

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Moderate this audit note:\n\n{text}"}
        ],
        temperature=0.0,
    )

    result_text = message.content[0].text if message.content else "{}"

    # Parse the JSON response
    import json

    try:
        result = json.loads(result_text)
    except json.JSONDecodeError:
        result = {
            "flagged": False,
            "categories": {},
            "risk_level": "unknown",
            "explanation": "Could not parse moderation result.",
            "redacted_text": text,
        }

    result["text"] = text
    result["model"] = model
    result["provider"] = "anthropic"

    logger.info(
        "Moderated text with Anthropic %s: flagged=%s, risk=%s",
        model,
        result.get("flagged"),
        result.get("risk_level"),
    )

    return result


def moderate_audit_notes(
    events: Optional[List[AuditEvent]] = None,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Moderate notes from federated login audit events.
    """
    if events is None:
        audit_logger = get_audit_logger()
        events = audit_logger.get_events()

    results = []
    for event in events:
        if event.notes:
            moderation = moderate_text(event.notes, api_key=api_key)
            moderation["event_id"] = event.event_id
            moderation["event_type"] = event.event_type
            results.append(moderation)

    return results


def moderate_free_text_claims(
    claims_text: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate free-text user profile claims or notes.
    """
    return moderate_text(claims_text, api_key=api_key)
