import boto3
from datetime import timedelta


def presigned_download(bucket_name, object_key, expiration=timedelta(hours=1)):
    s3 = boto3.client("s3")
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration.total_seconds(),
    )
    return url
