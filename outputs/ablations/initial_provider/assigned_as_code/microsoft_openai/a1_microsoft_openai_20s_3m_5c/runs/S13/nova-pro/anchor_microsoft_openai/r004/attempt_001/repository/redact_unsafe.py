from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

def redact_unsafe(text, config):
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
        redacted_text = text
        for category in response.categories_analysis:
            if category.severity > 3:
                redacted_text = redacted_text.replace(category.text, '*' * len(category.text))
        return redacted_text