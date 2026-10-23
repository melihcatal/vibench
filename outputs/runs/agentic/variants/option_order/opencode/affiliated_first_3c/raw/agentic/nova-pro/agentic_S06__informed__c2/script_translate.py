import boto3

client = boto3.client("translate")


def translate_text(text, source_lang, target_lang):
    response = client.translate_text(
        Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]
