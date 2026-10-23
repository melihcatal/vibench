import boto3


def collect_platform_metadata(response):
    metadata = {
        "usage": response['usage'],
        "resourceId": response['modelId'],
        "modelHandle": response['modelId'],
    }
    return metadata