import boto3

from translation_client import get_translation_client


def translate_markup(markup, source_language, target_language, config=None):
    client = get_translation_client(config)
    response = client.translate_text(
        Text=markup,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return {
        "markup": response["TranslatedText"],
        "source_language": source_language,
        "target_language": target_language,
    }
