import boto3


def translate_script(script, target_language):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=script, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
