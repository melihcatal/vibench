# [LATER-STEP] log_text_safety.py
"""Check selected log message text for unsafe content."""

from __future__ import annotations
from observability_models import LogResponse
from typing import List, Dict

# Simulated provider client - IBM Watsonx Guardrails guardrails API
# (Replace with real SDK if integrating)
# For illustration we use a placeholder function that always returns safe.


def is_safe(text: str) -> bool:
    """Placeholder safety check.

    Real implementation would call the provider API and inspect the response.
    """
    # Example provider: watsonx.ai guardrails
    # from ibm_watsonx_ai.resources.v1.ai_services import Guardrails
    # client = Guardrails()
    # result = client.check(text=text)
    # return result.is_safe
    return True  # Assume safe for demo


def filter_unsafe_logs(response: LogResponse) -> List[Dict[str, Any]]:
    """Return only the logs whose text passes the safety filter.

    Args:
        response (LogResponse): Normalized log events.

    Returns:
        List[Dict[str, Any]]: Unsafed log messages.
    """
    return [log for log in response.as_list() if is_safe(log.get("message", ""))]
