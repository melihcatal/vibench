from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_client, load_safety_config


def moderation_summary(payload, config=None):
    config = load_safety_config(config)
    items = (payload or {}).get('items', [])
    summary = {'total': len(items), 'flagged': 0, 'allowed': 0}
    with get_client(config) as client:
        for item in items:
            text = item.get('text', '')
            response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='FourSeverityLevels'))
            score = max((category.severity for category in response.categories_analysis), default=0)
            if score >= 2:
                summary['flagged'] += 1
            else:
                summary['allowed'] += 1
    return summary
