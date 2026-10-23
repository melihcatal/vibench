import boto3

def collect_platform_metadata(response):
    metadata = {
        'usage': response['usageMetadata'],
        'modelId': response['modelId']
    }
    return metadata