from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import make_client, normalize_payload


def moderation_summary(payload, config=None):
    payload = normalize_payload(payload)
    with make_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=payload["text"], output_type="EightSeverityLevels"))
    toxicity = max((category.severity for category in response.categories_analysis), default=0) / 7
    return {"summary": f"toxicity={toxicity:.3f}", "toxicity": toxicity}
