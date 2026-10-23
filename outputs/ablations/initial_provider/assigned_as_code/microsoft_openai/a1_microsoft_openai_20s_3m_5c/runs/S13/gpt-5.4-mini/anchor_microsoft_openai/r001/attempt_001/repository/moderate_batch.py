from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import make_client, normalize_payload


def moderate_batch(payload, config=None):
    payload = normalize_payload(payload)
    with make_client(config) as client:
        decisions = []
        for text in payload["texts"]:
            response = client.analyze_text(AnalyzeTextOptions(text=text, output_type="EightSeverityLevels"))
            toxicity = max((category.severity for category in response.categories_analysis), default=0) / 7
            decisions.append({"text": text, "toxicity": toxicity, "allow": toxicity < 0.5})
    return {"decisions": decisions}
