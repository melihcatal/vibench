import re
from safety_models import SafetyResponse


def redact_unsafe(text: str, response: SafetyResponse, threshold: float = 0.5) -> str:
    redacted_text = text
    for label, score in response.labels.items():
        if score > threshold:
            redacted_text = re.sub(label, "[REDACTED]", redacted_text)
    return redacted_text
