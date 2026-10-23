from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import create_client
from safety_models import normalize_text_payload, normalize_thresholds


def safety_threshold(payload, config=None):
    payload = normalize_text_payload(payload)
    thresholds = normalize_thresholds(config)
    with create_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
    category_scores = {category.category: category.severity / 7 for category in response.categories_analysis}
    allow = all(category_scores.get(category, 0) <= threshold for category, threshold in thresholds.items())
    return {'allow': allow, 'scores': category_scores}
