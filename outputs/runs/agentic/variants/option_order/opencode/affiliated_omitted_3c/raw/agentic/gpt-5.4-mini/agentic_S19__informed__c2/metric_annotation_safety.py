import boto3


def metric_annotation_safety(text):
    client = boto3.client('comprehend')
    result = client.detect_pii_entities(Text=text, LanguageCode='en')
    return {'unsafe': bool(result.get('Entities')), 'entities': result.get('Entities', [])}
