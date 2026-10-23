import boto3


def translate_markup(markup, source_lang, target_lang):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=markup, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]
