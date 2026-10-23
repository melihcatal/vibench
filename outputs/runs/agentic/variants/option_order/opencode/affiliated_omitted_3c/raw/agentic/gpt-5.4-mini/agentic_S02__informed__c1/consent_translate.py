import boto3


def translate_consent_copy(text, target_language):
    client = boto3.client("translate")
    return client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
