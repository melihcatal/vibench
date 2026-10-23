# [SAME-SCENARIO] redact_unsafe.py

import os
import re
from typing import List, Tuple

from safety_client import SafetyClient
from safety_models import TextModerationResult, UnsafeSpan

CLIENT = SafetyClient()

def redact_unsafe(text: str) -> Tuple[str, List[UnsafeSpan]]:
    """Flag or redact unsafe spans in the provided text.
    Returns the (possibly redacted) text and a list of unsafe spans.
    Unsafe spans are identified via the moderation result and masked with '[REDACTED]'.
    """
    result: TextModerationResult = CLIENT.check_content(text)
    span_list: List[UnsafeSpan] = []
    # Simple illustration: combine all flagged categories into spans
    unsafe_chars = set()
    for cat, score in result.detailed.items():
        if score > result.thresholds.get(cat, 0.5):
            # naive span: whole document for demonstration
            span_list.append(UnsafeSpan(start=0, end=len(text), category=cat, score=score))
    # Redact all flagged portions (here the whole text) with a placeholder
    redacted = ''.join('[REDACTED]' if sp.start <= i < sp.end else text[i]
                       for i in range(len(text))
                       for sp in span_list)
    return redacted, span_list
