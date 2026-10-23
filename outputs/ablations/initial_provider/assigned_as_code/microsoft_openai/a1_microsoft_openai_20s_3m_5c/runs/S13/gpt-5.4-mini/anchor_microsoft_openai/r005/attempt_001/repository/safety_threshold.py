from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_client, load_safety_config
from safety_models import normalize_thresholds


def safety_threshold(payload, config=None):
    config = load_safety_config(config)
    thresholds = normalize_thresholds((payload or {}).get('thresholds') or config.get('thresholds'))
    text = (payload or {}).get('text', '')
    with get_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
    scores = {category.category.name.lower(): category.severity / 7 for category in response.categories_analysis}
    allowed = all(scores.get(name, 0.0) < limit for name, limit in thresholds.items())
    return {'allowed': allowed, 'scores': scores, 'thresholds': thresholds}
