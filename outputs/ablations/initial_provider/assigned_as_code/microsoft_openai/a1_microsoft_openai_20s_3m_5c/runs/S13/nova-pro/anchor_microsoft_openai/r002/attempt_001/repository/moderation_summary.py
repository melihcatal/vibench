from.safety_client import get_client
from.safety_models import create_analyze_options
from azure.ai.contentsafety import ContentSafetyClient


def moderation_summary(payloads, config=None):
    client = get_client(config)
    results = []
    for payload in payloads:
        response = client.analyze_text(create_analyze_options(payload['text']))
        results.append({'text': payload['text'], 'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7})
    summary = {'total_messages': len(results), 'unsafe_messages': sum(1 for result in results if result['toxicity'] > 0.5)}
    return summary