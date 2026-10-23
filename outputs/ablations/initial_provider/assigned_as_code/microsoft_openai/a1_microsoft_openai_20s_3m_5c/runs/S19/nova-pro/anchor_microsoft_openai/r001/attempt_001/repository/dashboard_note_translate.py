import boto3

def translate_dashboard_note(payload, config=None):
    config = config or {}
    translate = boto3.client('translate', region_name=config.get('region', 'us-west-2'))
    response = translate.translate_text(Text=payload['note'], SourceLanguageCode='en', TargetLanguageCode=payload['target_language'])
    return response