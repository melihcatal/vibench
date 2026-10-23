import boto3


def object_metadata(bucket_name, object_key):
    s3 = boto3.client("s3")
    metadata = s3.head_object(Bucket=bucket_name, Key=object_key)
    return metadata
