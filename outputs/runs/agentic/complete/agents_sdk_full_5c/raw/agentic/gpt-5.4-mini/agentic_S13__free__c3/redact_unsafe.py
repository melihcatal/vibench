import re
from typing import Iterable

from safety_client import configure_client
from safety_models import ModerationRequest
from moderate_text import moderate_text

REDACTION_TOKEN = "[REDACTED]"


def redact_unsafe(text: str, sensitive_terms: Iterable[str] = ()) -> str:
    configure_client()
    decision = moderate_text(ModerationRequest(text=text))
    redacted = text
    if not decision.allow:
        for term in sensitive_terms:
            redacted = re.sub(re.escape(term), REDACTION_TOKEN, redacted, flags=re.IGNORECASE)
    return redacted if decision.allow else redacted
