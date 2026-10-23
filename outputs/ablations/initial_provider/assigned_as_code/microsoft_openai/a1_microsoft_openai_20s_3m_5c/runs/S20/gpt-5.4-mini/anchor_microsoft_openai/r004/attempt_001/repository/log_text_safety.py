from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def log_text_safety(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(endpoint=config["endpoint"], credential=AzureKeyCredential(config["key"]))
    response = client.analyze_text(payload["text"], categories=["Hate", "SelfHarm", "Sexual", "Violence"])
    return {"unsafe": any(item.severity > 0 for item in response.categories_analysis)}
