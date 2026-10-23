from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from messaging_client import load_messaging_config


def message_safety(payload, config=None):
    cfg = load_messaging_config(config)
    client = ContentSafetyClient(endpoint=cfg.get("content_safety_endpoint", "https://example.cognitiveservices.azure.com/"), credential=AzureKeyCredential(cfg.get("content_safety_key", "")))
    result = client.analyze_text(payload_text=str(payload))
    return {"unsafe": any(getattr(item, "severity", 0) > 0 for item in result.categories_analysis)}
