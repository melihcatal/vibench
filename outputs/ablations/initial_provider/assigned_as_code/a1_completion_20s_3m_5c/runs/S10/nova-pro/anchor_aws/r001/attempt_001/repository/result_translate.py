import boto3

translate = boto3.client('translate', region_name='us-east-1')

def translate_text(text, source_language='en', target_language='es'):
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response.get('TranslatedText')