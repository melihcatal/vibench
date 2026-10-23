from storage_client import build_list_response, get_s3_client


def list_prefix(bucket: str, prefix: str = ""):
    client = get_s3_client()
    paginator = client.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get("Contents", []):
            keys.append(item["Key"])
    return build_list_response(bucket, prefix, keys)
