import re
from safety_client import SafetyClient


def redact_unsafe(text: str) -> str:
    """Flag or redact unsafe spans from the supplied text.

    Returns the text with any unsafe span replaced by [REDACTED].
    """
    client = SafetyClient()
    unsafe_spans = client.find_unsafe_spans(text)

    def repl(match):
        return "[REDACTED]"

    pattern = re.compile("|".join(re.escape(span) for span in unsafe_spans))
    return pattern.sub(repl, text)
