from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential


def safety_threshold(payload, config=None, threshold=0.5):
    config = config or {}
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
        toxicity = max((category.severity for category in response.categories_analysis), default=0) / 7
        return toxicity <= threshold