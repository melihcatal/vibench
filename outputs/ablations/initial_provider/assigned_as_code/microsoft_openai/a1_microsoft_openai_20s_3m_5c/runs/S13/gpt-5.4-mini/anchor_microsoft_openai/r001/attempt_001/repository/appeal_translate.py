from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from safety_client import normalize_payload


def appeal_translate(payload, config=None):
    payload = normalize_payload(payload)
    config = config or {}
    client = TextTranslationClient(
        endpoint=config["translation_endpoint"],
        credential=AzureKeyCredential(config["translation_key"]),
    )
    target = payload["target_language"] or config.get("target_language", "en")
    result = client.translate(content=[payload["text"]], to=[target])
    return {"translation": result[0].translations[0].text if result else ""}
