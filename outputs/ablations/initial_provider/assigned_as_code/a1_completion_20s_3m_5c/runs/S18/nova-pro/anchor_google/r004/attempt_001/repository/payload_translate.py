import boto3


def translate_payload(payload, target_language):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=payload,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']