from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from.safety_client import get_client


def safety_threshold(payload, config=None):
    client = get_client(config)
    response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
    toxicity_scores = [category.severity for category in response.categories_analysis]
    max_toxicity = max(toxicity_scores, default=0)
    return {'allow': max_toxicity <= 3}