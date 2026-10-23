import re
from typing import Dict

from google.cloud import contentmoderator_v1


def is_safe_message(payload: str) -> Dict[str, object]:
    client = contentmoderator_v1.ContentModeratorClient()
    unsafe_patterns = [r"\bviolence\b", r"\bhate\b", r"\bself-harm\b"]
    matched = [pattern for pattern in unsafe_patterns if re.search(pattern, payload, re.IGNORECASE)]
    return {"safe": not matched, "matched_patterns": matched, "provider": client.__class__.__name__}
