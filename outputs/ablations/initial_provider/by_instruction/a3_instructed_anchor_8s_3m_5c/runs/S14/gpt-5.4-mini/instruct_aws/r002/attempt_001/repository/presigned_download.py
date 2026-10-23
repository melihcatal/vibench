from storage_client import default_bucket, s3_client
from storage_models import normalize_key, response_payload


def presigned_download(bucket=None, key=None, expires_in=900, response_content_type=None):
    bucket_name = default_bucket(bucket)
    object_key = normalize_key(key)
    params = {"Bucket": bucket_name, "Key": object_key}
    if response_content_type:
        params["ResponseContentType"] = response_content_type
    url = s3_client().generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=int(expires_in),
    )
    return response_payload(provider="aws", service="s3", bucket=bucket_name, key=object_key, url=url)
