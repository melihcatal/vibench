from safety_client import score_text


def redact_unsafe(text, categories=None, thresholds=None, redaction_token="[REDACTED]"):
    decision = score_text(text, categories=categories, thresholds=thresholds)
    if decision.allowed:
        return {"text": text, "redacted": False, "decision": decision}
    return {"text": redaction_token, "redacted": True, "decision": decision}
