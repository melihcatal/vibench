import boto3


def translate_text(text):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode="es"
    )
    return response.get("TranslatedText")
