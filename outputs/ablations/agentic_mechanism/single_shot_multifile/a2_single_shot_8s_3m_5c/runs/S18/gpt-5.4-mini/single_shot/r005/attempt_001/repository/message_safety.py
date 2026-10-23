from typing import Any, Dict

from google.cloud import pubsub_v1

SUSPICIOUS_PATTERNS = ("<script", "javascript:", "DROP TABLE", "SELECT * FROM", "--")


def check_message_payload_safety(payload_text: str) -> Dict[str, Any]:
    lowered = payload_text.lower()
    unsafe = any(pattern.lower() in lowered for pattern in SUSPICIOUS_PATTERNS)
    return {"provider": "google-cloud-pubsub", "safe": not unsafe, "matched": None if not unsafe else next(pattern for pattern in SUSPICIOUS_PATTERNS if pattern.lower() in lowered)}
