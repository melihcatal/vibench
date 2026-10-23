from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from.safety_client import get_content_safety_client


def safety_threshold(payload, config=None):
    client = get_content_safety_client(config)
    response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
    decision = 'ALLOW'
    for category in response.categories_analysis:
        if category.severity > 3:
            decision = 'BLOCK'
            break
    return {'decision': decision}