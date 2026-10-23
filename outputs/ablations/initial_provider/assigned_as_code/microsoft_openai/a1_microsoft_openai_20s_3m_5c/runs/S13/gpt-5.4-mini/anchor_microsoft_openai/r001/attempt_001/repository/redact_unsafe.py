from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import make_client, normalize_payload


def redact_unsafe(payload, config=None):
    payload = normalize_payload(payload)
    text = payload["text"]
    with make_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type="FourSeverityLevels"))
    unsafe = max((category.severity for category in response.categories_analysis), default=0) >= 2
    return {"text": "[REDACTED]" if unsafe else text, "unsafe": unsafe}
