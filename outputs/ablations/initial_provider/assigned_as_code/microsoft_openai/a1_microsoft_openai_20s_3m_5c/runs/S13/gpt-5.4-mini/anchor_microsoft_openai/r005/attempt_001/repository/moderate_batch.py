from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_client, load_safety_config
from safety_models import SafetyBatchRequest


def moderate_batch(payload, config=None):
    config = load_safety_config(config)
    request = SafetyBatchRequest.from_payload(payload)
    decisions = []
    with get_client(config) as client:
        for text in request.messages:
            response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
            score = max((category.severity for category in response.categories_analysis), default=0) / 7
            decisions.append({'text': text, 'allowed': score < 0.5, 'score': score})
    return {'decisions': decisions}
