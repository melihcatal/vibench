from translation_client import get_aws_translate_client, load_translation_config, normalize_language_code
from translation_models import TranslationResponse, normalize_text


def translate_dictionary_values(data: dict[str, object], source_language: str | None = None, target_language: str | None = None) -> dict[str, object]:
    config = load_translation_config()
    client = get_aws_translate_client()
    target = normalize_language_code(target_language) or config.default_target_language
    source = normalize_language_code(source_language or config.default_source_language)
    translated: dict[str, object] = {}
    for key, value in data.items():
        if isinstance(value, str):
            kwargs = {"Text": normalize_text(value), "TargetLanguageCode": target}
            if source:
                kwargs["SourceLanguageCode"] = source
            translated[key] = client.translate_text(**kwargs)["TranslatedText"]
        else:
            translated[key] = value
    return translated
