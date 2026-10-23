from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

def apply_safety_threshold(text, config, threshold=0.5):
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
        toxicity_score = max((category.severity for category in response.categories_analysis), default=0) / 7
        return toxicity_score <= threshold