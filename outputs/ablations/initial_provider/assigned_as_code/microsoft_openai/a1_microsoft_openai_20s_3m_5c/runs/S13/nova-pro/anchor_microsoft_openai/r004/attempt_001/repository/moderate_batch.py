from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

def moderate_batch(messages, config):
    results = []
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        for message in messages:
            response = client.analyze_text(AnalyzeTextOptions(text=message['text'], output_type='EightSeverityLevels'))
            results.append({'id': message['id'], 'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7})
    return results