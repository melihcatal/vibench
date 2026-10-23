import boto3


def translate_payload(message):
    translate_client = boto3.client("translate")
    response = translate_client.translate_text(
        Text=message, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response
