import re

def redact_unsafe(text: str, span_pattern: str = r"\b(?:harassment|threat|hate)\b") -> str:
    """Replace flagged unsafe spans with [REDACTED].

    Args:
        text: Input text.
        span_pattern: Regex pattern matching unsafe spans.

    Returns:
        Text with unsafe spans replaced by '[REDACTED]'.
    """
    return re.sub(span_pattern, "[REDACTED]", text)
