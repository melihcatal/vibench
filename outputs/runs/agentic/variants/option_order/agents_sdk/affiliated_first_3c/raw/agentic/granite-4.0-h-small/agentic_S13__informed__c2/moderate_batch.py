# [SAME-SCENARIO] moderate_batch.py

import os
from safety_client import SafetyClient
from safety_models import TextModerationResult, BatchModerationBatch

CLIENT = SafetyClient()

def moderate_batch(texts: list[str]) -> dict[str, TextModerationResult]:
    """Moderate a batch of user messages.
    Returns a dict mapping each original text to its moderation result.
    """
    results = {}
    for txt in texts:
        decision = CLIENT.check_content(txt)
        results[txt] = decision
    return results
