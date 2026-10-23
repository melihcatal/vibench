from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_client


def safety_threshold(payload, config=None):
    config = config or {}
    thresholds = config.get('thresholds', {})
    with get_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
    scores = {category.category: category.severity / 7 for category in response.categories_analysis}
    allowed = all(scores.get(name, 0.0) <= float(limit) for name, limit in thresholds.items())
    return {'allowed': allowed, 'scores': scores}
