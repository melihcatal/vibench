from safety_client import AzureContentSafetyClient
from safety_models import RedactionResult, RedactionSpan, normalize_text


def redact_unsafe(text: str) -> RedactionResult:
    client = AzureContentSafetyClient()
    payload = client.redact(normalize_text(text))
    spans = []
    for item in payload.get("spans", payload.get("redactions", [])):
        spans.append(
            RedactionSpan(
                start=int(item.get("start", 0)),
                end=int(item.get("end", 0)),
                category=str(item.get("category", item.get("type", "unsafe"))),
            )
        )
    return RedactionResult(
        text=str(payload.get("redactedText", payload.get("text", text))),
        spans=spans,
        raw=payload,
    )
