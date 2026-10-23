import boto3

from vision_client import get_vision_client


def alt_text_translate(payload, config=None):
    client = get_vision_client(config)
    translate_client = boto3.client('translate', region_name=config.get('region'))
    description = payload['description']
    response = translate_client.translate_text(
        Text=description,
        SourceLanguageCode='en',
        TargetLanguageCode='es'
    )
    return {'translated_description': response['TranslatedText']}