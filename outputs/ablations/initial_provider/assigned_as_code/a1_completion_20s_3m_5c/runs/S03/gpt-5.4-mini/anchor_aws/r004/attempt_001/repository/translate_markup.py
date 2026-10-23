import boto3

from translation_models import normalize_language_code, normalize_text


def translate_markup(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(
        Text=normalize_text(payload["markup"]),
        SourceLanguageCode=normalize_language_code(payload["source_language"]),
        TargetLanguageCode=normalize_language_code(payload["target_language"]),
        Settings={"Formality": config.get("formality", "informal")},
    )
    return {
        "markup": response["TranslatedText"],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
