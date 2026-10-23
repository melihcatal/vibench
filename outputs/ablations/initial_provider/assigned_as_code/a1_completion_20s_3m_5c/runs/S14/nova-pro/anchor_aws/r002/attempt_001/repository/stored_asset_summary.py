import boto3
from botocore.exceptions import ClientError


def summarize_stored_asset(object_name):
    comprehend_client = boto3.client('comprehend', region_name='your-region')
    try:
        with open(object_name, 'r') as f:
            text = f.read()
        response = comprehend_client.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
    except ClientError as e:
        raise e
    return response