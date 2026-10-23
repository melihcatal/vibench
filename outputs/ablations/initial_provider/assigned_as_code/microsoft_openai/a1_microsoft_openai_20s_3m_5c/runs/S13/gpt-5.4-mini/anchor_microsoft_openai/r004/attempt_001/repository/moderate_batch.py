from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import create_client
from safety_models import normalize_messages


def moderate_batch(payload, config=None):
    messages = normalize_messages(payload)
    with create_client(config) as client:
        decisions = []
        for message in messages:
            text = message.get('text', '')
            response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
            score = max((category.severity for category in response.categories_analysis), default=0) / 7
            decisions.append({'text': text, 'toxicity': score, 'allowed': score < 0.5})
    return {'decisions': decisions}
