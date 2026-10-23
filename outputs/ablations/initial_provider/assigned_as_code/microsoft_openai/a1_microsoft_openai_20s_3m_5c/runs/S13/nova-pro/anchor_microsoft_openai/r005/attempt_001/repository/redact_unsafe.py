from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential


def redact_unsafe(payload, config=None):
    config = config or {}
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
        if max((category.severity for category in response.categories_analysis), default=0) > 3:
            redacted_text = 'REDACTED'
        else:
            redacted_text = payload['text']
    return {'redacted_text': redacted_text}