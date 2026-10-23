import boto3
from botocore.exceptions import ClientError


def embed_object_metadata(object_name, metadata):
    comprehend_client = boto3.client('comprehend', region_name='your-region')
    try:
        response = comprehend_client.detect_dominant_language(
            Text=metadata
        )
    except ClientError as e:
        raise e
    return response