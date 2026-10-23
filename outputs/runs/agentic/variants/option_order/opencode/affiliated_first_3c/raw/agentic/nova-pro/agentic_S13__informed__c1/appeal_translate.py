import boto3


def appeal_translate(text):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
