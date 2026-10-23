import azure.ai.contentsafety
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def script_safety(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(config["endpoint"], AzureKeyCredential(config["key"]))
    result = client.analyze_text(azure.ai.contentsafety.AnalyzeTextOptions(text=payload["text"]))
    categories = []
    for item in result.categories_analysis:
        categories.append({"category": item.category, "severity": item.severity})
    return {"categories": categories}
