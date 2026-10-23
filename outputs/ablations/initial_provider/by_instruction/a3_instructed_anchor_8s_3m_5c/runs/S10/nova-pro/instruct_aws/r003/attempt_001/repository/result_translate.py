import boto3

def translate_result(text, target_language='es'):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response.get('TranslatedText')