import boto3


def translate_payload(message, config=None):
    config = config or {}
    translate = boto3.client('translate', region_name=config['region'])
    response = translate.translate_text(
        Text=message['text'],
        SourceLanguageCode='en',
        TargetLanguageCode=config['target_language']
    )
    message['translated_text'] = response['TranslatedText']
    return message