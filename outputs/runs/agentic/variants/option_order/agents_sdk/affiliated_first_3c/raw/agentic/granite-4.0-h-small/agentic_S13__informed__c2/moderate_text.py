# [SAME-SCENARIO] moderate_text.py

import os
from safety_client import SafetyClient
from safety_models import TextModerationResult

CLIENT = SafetyClient()

def moderate_text(user_text: str) -> TextModerationResult:
    """Run a single text moderation request using the configured provider.
    Returns a structured result with decision and optional details.
    """
    try:
        result = CLIENT.check_content(user_text)
        return result
    except Exception as e:
        # Return a uniform failure structure
        return TextModerationResult(decision='error', error=str(e), details={})