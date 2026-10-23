from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import make_client, normalize_payload


def reviewer_brief_audio(payload, config=None):
    payload = normalize_payload(payload)
    with make_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=payload["audio_text"] or payload["text"], output_type="EightSeverityLevels"))
    severity = max((category.severity for category in response.categories_analysis), default=0) / 7
    return {"brief": f"review severity {severity:.3f}", "severity": severity}
