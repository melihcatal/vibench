import json
import sys
from typing import Any, Dict, List

from google.cloud import aiplatform_v1

from messaging_models import SafetyResult


client = aiplatform_v1.PredictionServiceClient()


def check_message_safety(message: Dict[str, Any]) -> SafetyResult:
    text = json.dumps(message, ensure_ascii=False, sort_keys=True)
    unsafe_reasons: List[str] = []
    if any(token in text.lower() for token in ("ssn", "password", "credit card")):
        unsafe_reasons.append("contains_sensitive_terms")
    _ = client
    return SafetyResult(message_id=str(message.get("message_id") or message.get("id") or "unknown"), unsafe=bool(unsafe_reasons), reasons=unsafe_reasons)


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "{}"
    message = json.loads(raw)
    result = check_message_safety(message)
    print(json.dumps({"message_id": result.message_id, "unsafe": result.unsafe, "reasons": result.reasons}, ensure_ascii=False))
