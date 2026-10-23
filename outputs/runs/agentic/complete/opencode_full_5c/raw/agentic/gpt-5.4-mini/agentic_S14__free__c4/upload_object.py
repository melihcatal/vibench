import argparse

from storage_client import get_bucket_name, get_object_key, get_s3_client
from storage_models import normalize_bytes, normalize_metadata


def upload_object(bucket=None, key=None, body=None, content_type=None, metadata=None):
    s3 = get_s3_client()
    bucket = get_bucket_name(bucket)
    key = get_object_key(key)
    payload = normalize_bytes(body)
    kwargs = {"Bucket": bucket, "Key": key, "Body": payload}
    if content_type:
        kwargs["ContentType"] = content_type
    normalized = normalize_metadata(metadata)
    if normalized:
        kwargs["Metadata"] = normalized
    return s3.put_object(**kwargs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("path")
    args = parser.parse_args()
    with open(args.path, "rb") as f:
        upload_object(args.bucket, args.key, f.read())


if __name__ == "__main__":
    main()
