import re
from typing import List, Dict
from observability_models import LogEvent


def contains_unsafe_content(events: List[Dict[str, Any]]) -> bool:
    """Check selected log message text for unsafe content.

    Provider: Custom regex-based content filter (no external service).
    """
    unsafe_patterns = [
        r"password=\\S+",
        r"secret=\\S+",
        r"(ssh|api)_key=\\S+",
        r"access_token=\\S+",
    ]
    for evt in events:
        msg = evt.get("message", "")
        for pattern in unsafe_patterns:
            if re.search(pattern, msg, re.IGNORECASE):
                return True
    return False
