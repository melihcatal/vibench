import boto3


def appeal_translate(payload, config=None):
    config = config or {}
    client = boto3.client('translate', region_name=config.get('region', 'us-east-1'))
    response = client.translate_text(Text=payload['text'], SourceLanguageCode='en', TargetLanguageCode=config.get('target_language', 'es'))
    return {'translated_text': response['TranslatedText']}