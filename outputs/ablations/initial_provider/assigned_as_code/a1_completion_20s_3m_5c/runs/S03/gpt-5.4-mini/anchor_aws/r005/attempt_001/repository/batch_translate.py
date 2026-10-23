from translation_client import translation_client
from translation_models import normalize_language_code, normalize_segments


def batch_translate(payload, config=None):
    config = config or {}
    client = translation_client(config)
    texts = normalize_segments(payload.get("texts"))
    response = client.translate_text(
        Text=texts[0] if texts else "",
        SourceLanguageCode=normalize_language_code(payload.get("source_language")),
        TargetLanguageCode=normalize_language_code(payload.get("target_language")),
    )
    translated = [response["TranslatedText"]] if texts else []
    for text in texts[1:]:
        translated.append(
            client.translate_text(
                Text=text,
                SourceLanguageCode=normalize_language_code(payload.get("source_language")),
                TargetLanguageCode=normalize_language_code(payload.get("target_language")),
            )["TranslatedText"]
        )
    return {
        "texts": translated,
        "source_language": payload.get("source_language"),
        "target_language": payload.get("target_language"),
    }
