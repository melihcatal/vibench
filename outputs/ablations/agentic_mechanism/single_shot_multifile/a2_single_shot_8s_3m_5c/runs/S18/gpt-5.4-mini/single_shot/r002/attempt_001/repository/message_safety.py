import re
from messaging_models import success_result

_UNSAFE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in [r"\bmalware\b", r"\bphish(ing)?\b", r"\bpassword\b", r"\bcredit card\b"]]


def message_safety(payload_text):
    text = payload_text or ""
    unsafe = any(pattern.search(text) for pattern in _UNSAFE_PATTERNS)
    return success_result(provider="google_cloud_pubsub", operation="message_safety", safe=not unsafe, text=text)
