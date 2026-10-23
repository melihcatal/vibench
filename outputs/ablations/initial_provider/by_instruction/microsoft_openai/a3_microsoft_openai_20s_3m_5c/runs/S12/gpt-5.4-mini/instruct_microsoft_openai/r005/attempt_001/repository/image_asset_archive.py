import os

import requests


S3_ENDPOINT = os.getenv("S3_ENDPOINT", "https://s3.amazonaws.com")


def image_asset_archive(bucket, key, content):
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not access_key or not secret_key:
        raise RuntimeError("AWS credentials are required")
    response = requests.put(
        f"{S3_ENDPOINT}/{bucket}/{key}",
        headers={"x-amz-content-sha256": "UNSIGNED-PAYLOAD"},
        data=content.encode("utf-8") if isinstance(content, str) else content,
        timeout=60,
    )
    response.raise_for_status()
    return {"bucket": bucket, "key": key, "status_code": response.status_code}
