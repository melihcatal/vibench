from safety_client import AzureContentSafetyClient
from safety_models import RedactionResult, RedactionSpan


client = AzureContentSafetyClient()


def redact_unsafe(text: str) -> RedactionResult:
    raw = client.redact_text(text)
    spans = []
    redacted_text = text
    for item in raw.get('text', {}).get('offsets', []) if isinstance(raw, dict) else []:
        spans.append(RedactionSpan(start=int(item.get('start', 0)), end=int(item.get('end', 0)), label=str(item.get('category', 'unsafe'))))
    if isinstance(raw, dict):
        redacted_text = raw.get('text', {}).get('value', text)
    return RedactionResult(redacted_text=redacted_text, spans=spans, raw=raw)
