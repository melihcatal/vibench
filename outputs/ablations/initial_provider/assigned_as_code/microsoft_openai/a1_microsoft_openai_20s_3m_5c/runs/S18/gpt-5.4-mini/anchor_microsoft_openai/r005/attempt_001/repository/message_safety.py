from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from messaging_client import load_messaging_config


def check_message_safety(text, config=None):
    cfg = load_messaging_config(config)
    client = ContentSafetyClient(cfg['safety_endpoint'], AzureKeyCredential(cfg['safety_key']))
    result = client.analyze_text(text)
    return {'unsafe': any(getattr(item, 'severity', 0) >= 2 for item in result.categories_analysis), 'result': result}
