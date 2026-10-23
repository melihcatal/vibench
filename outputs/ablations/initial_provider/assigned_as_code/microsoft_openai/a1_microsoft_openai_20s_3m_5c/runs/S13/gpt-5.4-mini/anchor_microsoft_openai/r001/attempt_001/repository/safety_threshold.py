from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import make_client, normalize_payload


def safety_threshold(payload, config=None):
    payload = normalize_payload(payload)
    thresholds = payload["thresholds"]
    with make_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=payload["text"], output_type="EightSeverityLevels"))
    severity = max((category.severity for category in response.categories_analysis), default=0) / 7
    limit = float(thresholds.get("toxicity", 0.5))
    return {"allow": severity <= limit, "toxicity": severity, "threshold": limit}
