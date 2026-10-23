import boto3


def create_presigned_download(object_name, config=None):
    config = config or {}
    client = boto3.client("s3", region_name=config.get("region"))
    presigned_url = client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': config['bucket'], 'Key': object_name},
        ExpiresIn=3600
    )
    return {"presigned_url": presigned_url}