from azure.ai.contentSafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from security_client import load_security_config


def payload_safety(payload, config=None):
    config = load_security_config(config)
    client = ContentSafetyClient(config.get('endpoint', ''), AzureKeyCredential(config.get('api_key', '')))
    text = payload.get('plaintext', b'')
    if isinstance(text, bytes):
        text = text.decode('utf-8', 'ignore')
    result = client.analyze_text({'text': text}) if hasattr(client, 'analyze_text') else None
    return {'safe': True if result is None else getattr(result, 'is_safe', True), 'provider': 'azure-ai-content-safety'}
