import boto3

def translate_consent(text, source_language_code, target_language_code):
    translate_client = boto3.client('translate')
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return result.get('TranslatedText')