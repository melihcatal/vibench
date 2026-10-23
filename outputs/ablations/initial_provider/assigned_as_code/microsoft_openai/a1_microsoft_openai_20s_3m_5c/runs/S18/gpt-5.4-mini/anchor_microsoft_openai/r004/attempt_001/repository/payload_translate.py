from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from messaging_client import load_messaging_config


def payload_translate(text, target_language, config=None):
    cfg = load_messaging_config(config)
    client = TextTranslationClient(endpoint=cfg.get("translator_endpoint", "https://api.cognitive.microsofttranslator.com"), credential=AzureKeyCredential(cfg.get("translator_key", "")))
    response = client.translate(content=[text], to=[target_language])
    return {"translated": response[0].translations[0].text}
