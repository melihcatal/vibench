from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import create_client
from safety_models import normalize_text_payload


def moderation_summary(payload, config=None):
    payload = normalize_text_payload(payload)
    with create_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='FourSeverityLevels'))
    top = max(response.categories_analysis, key=lambda category: category.severity, default=None)
    return {'summary': top.category if top else 'clean', 'severity': (top.severity if top else 0)}
