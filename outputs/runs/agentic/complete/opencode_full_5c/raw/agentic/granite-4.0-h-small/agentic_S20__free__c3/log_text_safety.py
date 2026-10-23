import re
import json
from observability_models import LogEvent


def text_contains_unsafe_content(message: str) -> bool:
    """Basic check for unsafe content (e.g., profanity, personal data).
    Returns True if unsafe content is detected.
    """
    # Example checks - expand as needed
    profanity = re.compile(r"\b(?:badword1|badword2)\b", re.IGNORECASE)
    if profanity.search(message):
        return True
    # Detect email addresses
    email_pat = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\b"
    if re.search(email_pat, message):
        return True
    return False


def filter_unsafe_logs(logs: List[LogEvent]) -> List[LogEvent]:
    """Remove logs with unsafe text."""
    return [l for l in logs if not text_contains_unsafe_content(l.message)]


# Example (removed)
# events = fetch_recent_logs(service="api", field="severity", value="info")
# safe = filter_unsafe_logs(events)
# print(json.dumps([e.__dict__ for e in safe], indent=2))
