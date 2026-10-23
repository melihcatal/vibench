from storage_client import client


def list_prefix(bucket: str, prefix: str = "") -> list[dict]:
    s3 = client()
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return resp.get("Contents", [])
