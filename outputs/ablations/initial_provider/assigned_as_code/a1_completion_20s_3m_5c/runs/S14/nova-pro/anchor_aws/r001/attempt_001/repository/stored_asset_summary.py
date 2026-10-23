import boto3

from storage_client import get_s3_client


def summarize_text(text, config=None):
    config = config or {}
    comprehend_client = boto3.client('comprehend', region_name=config.get('region'))

    response = comprehend_client.summarize_text(Text=text, LanguageCode='en')
    return response['SummaryText']