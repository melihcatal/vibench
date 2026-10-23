import boto3


def presigned_download(bucket_name, object_key, expiration=3600):
    s3 = boto3.client("s3")
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration,
    )
    print(f"Presigned URL: {url}")
    return url
