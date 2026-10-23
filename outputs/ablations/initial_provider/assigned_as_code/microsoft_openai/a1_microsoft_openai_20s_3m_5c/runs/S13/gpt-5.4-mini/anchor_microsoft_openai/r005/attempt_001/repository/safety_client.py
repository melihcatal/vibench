import os


def load_safety_config(config=None):
    config = config or {}
    return {
        "endpoint": config.get("endpoint") or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"),
        "api_key": config.get("api_key") or os.environ.get("AZURE_CONTENT_SAFETY_API_KEY"),
        "locale": config.get("locale") or os.environ.get("AZURE_CONTENT_SAFETY_LOCALE", "en"),
        "thresholds": config.get("thresholds") or {},
    }


def get_client(config):
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential

    return ContentSafetyClient(config["endpoint"], AzureKeyCredential(config["api_key"]))
