from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential


def moderate_batch(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key']))
    results = []
    for text_item in payload['texts']:
        response = client.analyze_text(AnalyzeTextOptions(text=text_item, output_type='EightSeverityLevels'))
        results.append({'text': text_item, 'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7})
    return results