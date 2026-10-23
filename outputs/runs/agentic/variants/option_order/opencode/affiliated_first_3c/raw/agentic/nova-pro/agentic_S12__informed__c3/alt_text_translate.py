import boto3


def translate_alt_text(text):
    translate_client = boto3.client("translate")
    translated_text = translate_client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return translated_text["TranslatedText"]
