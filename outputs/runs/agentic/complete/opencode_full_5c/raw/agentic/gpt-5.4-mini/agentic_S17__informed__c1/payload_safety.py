import boto3


def payload_safety(text, region=None):
    comprehend = boto3.client('comprehend', region_name=region or 'us-east-1')
    resp = comprehend.detect_toxic_content(TextSegments=[{'Text': text}])
    labels = resp.get('ResultList', [])
    unsafe = any(item.get('Toxicity') == 'HIGH' for item in labels)
    return {'unsafe': unsafe, 'labels': labels, 'provider': 'Amazon Comprehend'}
