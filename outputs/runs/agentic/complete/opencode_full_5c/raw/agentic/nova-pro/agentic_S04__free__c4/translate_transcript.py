import boto3

translate = boto3.client("translate", region_name="us-west-2")


def translate_text(text, source_lang, target_lang):
    response = translate.translate_text(
        Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]
