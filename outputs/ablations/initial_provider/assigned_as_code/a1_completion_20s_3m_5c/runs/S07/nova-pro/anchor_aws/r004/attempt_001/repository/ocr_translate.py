import boto3

def translate_text(text, source_language, target_language, config=None):
    config = config or {}
    client = boto3.client('translate', region_name=config.get('region'))
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response['TranslatedText']