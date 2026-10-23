from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_client
from safety_models import normalize_messages


def moderate_batch(payload, config=None):
    client = get_client(config)
    results = []
    with client:
        for item in normalize_messages(payload):
            response = client.analyze_text(AnalyzeTextOptions(text=item['text'], output_type='EightSeverityLevels'))
            severity = max((category.severity for category in response.categories_analysis), default=0) / 7
            results.append({'id': item['id'], 'allowed': severity < float((config or {}).get('threshold', 0.5)), 'severity': severity})
    return {'results': results}
