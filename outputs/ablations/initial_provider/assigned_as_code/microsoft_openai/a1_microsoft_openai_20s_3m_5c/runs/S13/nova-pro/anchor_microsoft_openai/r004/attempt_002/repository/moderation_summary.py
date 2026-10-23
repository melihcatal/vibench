from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential


def moderation_summary(payloads, config=None):
    config = config or {}
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        results = []
        for payload in payloads:
            response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
            results.append({'text': payload['text'], 'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7})
    return results