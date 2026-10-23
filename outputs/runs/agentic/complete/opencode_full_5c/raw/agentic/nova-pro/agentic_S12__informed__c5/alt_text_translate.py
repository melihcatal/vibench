import boto3


def alt_text_translate(text, target_language):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
