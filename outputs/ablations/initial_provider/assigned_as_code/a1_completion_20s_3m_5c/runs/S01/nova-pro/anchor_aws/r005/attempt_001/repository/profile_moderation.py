import boto3


def moderate_profile_text(text, config=None):
    config = config or {}
    client = boto3.client('comprehend', region_name=config.get('region'))
    response = client.detect_toxic_content(Text=text, LanguageCode='en')
    return response['Labels']
