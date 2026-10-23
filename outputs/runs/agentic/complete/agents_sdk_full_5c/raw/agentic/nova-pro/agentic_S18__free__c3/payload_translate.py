import boto3

def translate_payload(message, source_language, target_language):
    translate_client = boto3.client('translate')
    response = translate_client.translate_text(
        Text=message,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']