import boto3

def collect_metadata(response):
    metadata = response['ResponseMetadata']
    return metadata