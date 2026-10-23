import boto3


def translate_alt_text(text):
    client = boto3.client("translate")
    translated_text = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )["TranslatedText"]
    return translated_text
