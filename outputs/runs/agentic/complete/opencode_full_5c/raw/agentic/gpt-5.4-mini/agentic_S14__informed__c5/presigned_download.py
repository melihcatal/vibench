from storage_client import get_bucket_name, get_s3_client


def presigned_download(
    bucket=None, key=None, expires_in=3600, response_content_disposition=None
):
    client = get_s3_client()
    params = {"Bucket": get_bucket_name(bucket), "Key": key}
    if response_content_disposition:
        params["ResponseContentDisposition"] = response_content_disposition
    return client.generate_presigned_url(
        "get_object", Params=params, ExpiresIn=expires_in
    )
