import re

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def metric_annotation_safety(payload, config=None):
    config = config or {}
    text = payload.get('text') or payload.get('annotation') or ''
    endpoint = config.get('contentsafety_endpoint')
    key = config.get('contentsafety_key')
    if endpoint and key:
        with ContentSafetyClient(endpoint, AzureKeyCredential(key)) as client:
            result = client.analyze_text({'text': text})
        unsafe = any(getattr(item, 'severity', 0) >= 2 for item in getattr(result, 'categories_analysis', []))
    else:
        unsafe = bool(re.search(r'(?i)(password|secret|token|drop\s+table|<script)', text))
    return {'text': text, 'safe': not unsafe}
