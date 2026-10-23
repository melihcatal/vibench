import boto3


def extract_fields(text: str, config=None):
    config = config or {}
    client = boto3.client('comprehend', region_name=config.get('region'))
    response = client.detect_entities(Text=text, LanguageCode='en')
    fields = {entity['Type']: entity['Text'] for entity in response['Entities']}
    return fields