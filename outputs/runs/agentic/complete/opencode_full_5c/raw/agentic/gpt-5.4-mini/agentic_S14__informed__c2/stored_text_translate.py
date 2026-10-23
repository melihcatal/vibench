import boto3


def translate_stored_text(text: str, source_language_code: str = 'auto', target_language_code: str = 'en'):
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return response.get('TranslatedText')
