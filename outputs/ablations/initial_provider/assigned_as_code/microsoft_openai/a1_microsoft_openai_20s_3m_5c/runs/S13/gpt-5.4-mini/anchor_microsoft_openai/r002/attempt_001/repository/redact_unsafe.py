from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_client


def redact_unsafe(payload, config=None):
    config = config or {}
    text = payload['text']
    with get_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='FourSeverityLevels'))
    severity = max((category.severity for category in response.categories_analysis), default=0)
    if severity >= int(config.get('redact_threshold', 2)):
        return {'text': '[REDACTED]', 'redacted': True, 'severity': severity}
    return {'text': text, 'redacted': False, 'severity': severity}
