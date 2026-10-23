from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def log_message_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config["endpoint"], credential=AzureKeyCredential(config["key"]))
    response = client.translate(content=[payload["text"]], to=[payload["to"]])
    return {"translations": response}
