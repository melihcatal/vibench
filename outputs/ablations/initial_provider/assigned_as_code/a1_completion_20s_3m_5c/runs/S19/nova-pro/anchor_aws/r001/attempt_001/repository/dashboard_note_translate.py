import boto3


def dashboard_note_translate(payload, config=None):
    config = config or {}
    client = boto3.client('translate', region_name=config.get('region'))
    response = client.translate_text(Text=payload['note'], SourceLanguageCode='en', TargetLanguageCode=payload['target_language'])
    return {'translated_note': response['TranslatedText']}