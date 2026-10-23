import boto3


def runbook_translate(payload, config=None):
    client = boto3.client('translate', region_name=config.get('region'))
    response = client.translate_text(Text=payload['runbook_note'], SourceLanguageCode='en', TargetLanguageCode=payload['target_language'])
    return {'translated_text': response['TranslatedText']}