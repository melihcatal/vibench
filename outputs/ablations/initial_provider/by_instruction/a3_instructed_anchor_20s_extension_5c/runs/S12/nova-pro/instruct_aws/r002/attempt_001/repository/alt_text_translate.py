import boto3

def translate_alt_text(text, target_language='es'):
    translate_client = boto3.client('translate')
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']