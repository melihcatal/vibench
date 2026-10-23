import boto3
import summarize


def summarize_content_from_stored_asset(object_name, config=None):
    config = config or {}
    client = boto3.client('s3', region_name=config.get('region'))
    response = client.get_object(Bucket=config['bucket'], Key=object_name)
    document_content = response['Body'].read()
    text = document_content.decode('utf-8')
    summary = summarize.summarize(text)
    return summary