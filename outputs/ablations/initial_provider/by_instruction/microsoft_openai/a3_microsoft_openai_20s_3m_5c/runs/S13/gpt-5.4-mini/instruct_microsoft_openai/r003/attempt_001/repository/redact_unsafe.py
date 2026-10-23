from safety_client import moderate_text_request
from safety_models import RedactionResult, RedactionSpan


def redact_unsafe(text: str):
    decision = moderate_text_request(text)
    if not decision.flagged:
        return RedactionResult(redacted_text=text, spans=[], decision=decision)
    return RedactionResult(redacted_text="[REDACTED]", spans=[RedactionSpan(start=0, end=len(text))], decision=decision)
