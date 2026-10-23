import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

def metric_annotation_safety(text: str) -> dict:
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    response = client.analyze_text(
        AnalyzeTextOptions(text=text),
        category="Hate",
        block_threshold="Medium"
    )
    severity = getattr(response.hate, 'severity', None)
    is_unsafe = severity is not None and severity != 'safe'
    return {
        'is_unsafe': is_unsafe,
        'category': 'Hate',
        'severity': str(severity) if severity else 'none'
    }
