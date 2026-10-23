from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_client, load_safety_config


def redact_unsafe(payload, config=None):
    config = load_safety_config(config)
    text = (payload or {}).get('text', '')
    with get_client(config) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='FourSeverityLevels'))
    spans = []
    for category in response.categories_analysis:
        if getattr(category, 'severity', 0) >= 2:
            spans.append({'start': 0, 'end': len(text), 'label': category.category.name})
    redacted = text
    for span in sorted(spans, key=lambda item: item['start'], reverse=True):
        redacted = redacted[:span['start']] + '[REDACTED]' + redacted[span['end']:]
    return {'text': redacted, 'spans': spans}
