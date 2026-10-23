from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential


def moderate_batch(payloads, config=None):
    config = config or {}
    results = []
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        for payload in payloads:
            response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
            results.append({'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7})
    return results