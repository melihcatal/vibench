# redact_unsafe.py
import re
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse

def redact_unsafe(text: str) -> str:
    """Flag or redact unsafe spans detected by the moderation service.

    Uses Amazon Comprehend Toxicity as the concrete provider.
    """
    client = SafetyClient()
    request = ModerationRequest(text=text, language=client.detect_language(text))
    response = client.detect_toxicity(request)
    # Simple redaction: replace any flagged unsafe span with [REDACTED]
    unsafe_spans = response.unsafe_spans  # assume list of (start, end) tuples
    for start, end in sorted(unsafe_spans, key=lambda s: s[0], reverse=True):
        text = text[:start] + "[REDACTED]" + text[end:]
    return text

if __name__ == "__main__":
    sample = "This is a hateful comment."
    print(redact_unsafe(sample))
