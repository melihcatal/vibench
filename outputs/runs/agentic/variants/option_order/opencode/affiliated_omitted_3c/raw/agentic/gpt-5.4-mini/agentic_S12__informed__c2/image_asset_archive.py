import boto3


def archive_image_artifact(bucket, key, body):
    client = boto3.client('s3')
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {'bucket': bucket, 'key': key}
