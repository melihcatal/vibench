import boto3


def translate_message_payload(message, target_language):
    translate_client = boto3.client("translate")
    response = translate_client.translate_text(
        Text=message, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response
