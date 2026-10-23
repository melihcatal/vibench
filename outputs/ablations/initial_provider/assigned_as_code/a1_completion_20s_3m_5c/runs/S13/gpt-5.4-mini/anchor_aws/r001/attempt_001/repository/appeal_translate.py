from safety_client import get_translate_client
from safety_models import normalize_text


def appeal_translate(payload, config=None):
    config = config or {}
    client = get_translate_client(config)
    text = normalize_text(payload.get("text"))
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=config.get("source_language", "auto"),
        TargetLanguageCode=config.get("target_language", "en"),
    )
    return {"translated_text": response.get("TranslatedText", "")}
