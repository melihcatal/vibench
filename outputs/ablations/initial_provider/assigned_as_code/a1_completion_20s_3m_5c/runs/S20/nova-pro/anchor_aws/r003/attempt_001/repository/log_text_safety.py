import boto3

from observability_client import get_config


def log_text_safety(log_message):
    config = get_config()
    client = boto3.client('comprehend', region_name=config['region'])
    response = client.detect_toxic_content(
        TextSegments=[{
            'Text': log_message,
        }],
        LanguageCode='en',
    )
    return response['ResultList'][0]['ToxicContentDetected']