import boto3
from botocore.exceptions import ClientError

def check_metric_annotation_safety(payload, config=None):
    config = config or {}
    comprehend = boto3.client('comprehend', region_name=config.get('region', 'us-west-2'))
    try:
        response = comprehend.detect_sentiment(Text=payload['annotation'], LanguageCode='en')
        return response
    except ClientError as e:
        return {'error': str(e)}