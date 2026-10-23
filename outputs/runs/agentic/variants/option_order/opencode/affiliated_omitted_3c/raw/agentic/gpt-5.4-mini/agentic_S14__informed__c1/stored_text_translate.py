import boto3


def stored_text_translate(text, source_language_code, target_language_code):
    client = boto3.client("translate")
    return client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )["TranslatedText"]
