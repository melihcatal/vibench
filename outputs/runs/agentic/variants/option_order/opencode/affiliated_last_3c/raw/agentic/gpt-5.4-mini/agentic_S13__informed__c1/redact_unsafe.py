from safety_client import SafetyClient
from safety_models import RedactionResult, normalize_language, normalize_text


def redact_unsafe(text, language=None):
    client = SafetyClient()
    payload = {"text": normalize_text(text)}
    lang = normalize_language(language)
    if lang:
        payload["language"] = lang
    data = client.post("/contentsafety/text:analyze?api-version=2024-09-01", payload)
    redactions = []
    out = payload["text"]
    for item in data.get("categoriesAnalysis", []):
        if float(item.get("severity", 0)) >= 4:
            redactions.append(item)
    if redactions:
        out = "[REDACTED]"
    return RedactionResult(text=out, redactions=redactions, raw=data)
