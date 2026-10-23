from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def log_message_translate(payload, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config["endpoint"], credential=AzureKeyCredential(config["key"]))
    translated = client.translate([payload["text"]], to=[payload.get("target_locale", "en")])
    return {"translated_text": translated[0].translations[0].text}
