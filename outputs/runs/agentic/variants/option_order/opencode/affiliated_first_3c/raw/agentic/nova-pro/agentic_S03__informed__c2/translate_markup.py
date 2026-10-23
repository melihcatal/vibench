import boto3


def translate_markup(markup, source_lang, target_lang):
    client = boto3.client("translate")
    result = client.translate_text(
        Text=markup, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return result["TranslatedText"]
