from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from.safety_client import get_content_safety_client


def summarize_moderation(payloads, config=None):
    client = get_content_safety_client(config)
    results = []
    for payload in payloads:
        response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
        results.append({'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7})
    summary = {'average_toxicity': sum(result['toxicity'] for result in results) / len(results)}
    return summary