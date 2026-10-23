import boto3


def record_translate(text, source_lang, target_lang):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]
