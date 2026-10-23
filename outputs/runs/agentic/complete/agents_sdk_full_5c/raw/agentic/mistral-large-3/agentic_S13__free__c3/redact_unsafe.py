from typing import List, Optional
from safety_models import SafetyCategory, ModerationDecision, SafetySpan
from moderate_text import moderate_text


def redact_unsafe(
    text: str,
    categories: Optional[List[SafetyCategory]] = None,
    replacement: str = "[REDACTED]",
) -> str:
    """
    Flags or redacts unsafe spans from text using Google Content Safety API.
    """
    decision: ModerationDecision = moderate_text(text, categories=categories)
    spans = sorted(decision["spans"], key=lambda x: x["start"], reverse=True)
    
    text_list = list(text)
    for span in spans:
        start = span["start"]
        end = span["end"]
        text_list[start:end] = list(replacement)
    
    return "".join(text_list)