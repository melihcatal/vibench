import boto3


def translate_alt_text(alt_text):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=alt_text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
