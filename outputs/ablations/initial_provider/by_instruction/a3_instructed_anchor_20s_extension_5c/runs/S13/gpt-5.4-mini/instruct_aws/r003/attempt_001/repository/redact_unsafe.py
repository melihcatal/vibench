from typing import Dict, List

from safety_client import aws_comprehend_client, redaction_token
from safety_models import SafetyRedaction, normalize_text


def redact_unsafe(text: str) -> SafetyRedaction:
    client = aws_comprehend_client("comprehend")
    normalized = normalize_text(text)
    raw = client.detect_toxic_content(TextSegments=[{"Text": normalized}], LanguageCode="en")
    spans: List[Dict[str, object]] = []
    result = normalized
    token = redaction_token()
    for item in raw.get("ResultList", []):
        for span in item.get("ToxicContent", []):
            begin = int(span.get("BeginOffset", 0))
            end = int(span.get("EndOffset", 0))
            spans.append({"begin": begin, "end": end, "type": span.get("Type", "unsafe")})
            result = result[:begin] + token + result[end:]
    return SafetyRedaction(text=result, redacted_spans=spans, allow=not spans)
