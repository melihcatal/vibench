import boto3

translate_client = boto3.client('translate')

def translate_payload(text, target_language_code):
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language_code
    )
    return response