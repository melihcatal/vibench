import boto3

def translate_payload_text(text: str, source_language_code: str, target_language_code: str):
    translate_client = boto3.client('translate')  # AWS SDK import
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response['TranslatedText']
