import re
import json
from observability_client import get_log_client
from observability_models import LogEvent


def log_text_safety(
    logs: list[LogEvent], unsafe_patterns: list[str] = None
) -> list[LogEvent]:
    """Check selected log message text for unsafe content and redact if needed.

    Args:
        logs: List of log events (dictionaries).
        unsafe_patterns: Optional list of regex patterns that mark unsafe text.

    Returns:
        The same list with unsafe strings replaced by [REDACTED].
    """
    unsafe_patterns = unsafe_patterns or [
        r"(?i)password=[^\s]+",
        r"(?i)secret=[^\s]+",
        r"(?i)token=[^\s]+",
    ]
    compiled = [re.compile(p) for p in unsafe_patterns]
    for entry in logs:
        original = entry["message"]
        for pat in compiled:
            entry["message"] = pat.sub("[REDACTED]", original)
    return logs
