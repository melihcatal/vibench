import os
from pathlib import Path

import boto3


def archive_metric_snapshot(snapshot_path, bucket_name=None, object_key=None, region_name=None):
    path = Path(snapshot_path)
    if not path.is_file():
        raise FileNotFoundError(snapshot_path)

    bucket = bucket_name or os.environ.get("AWS_S3_BUCKET")
    if not bucket:
        raise ValueError("AWS_S3_BUCKET is required")

    key = object_key or path.name
    session = boto3.session.Session(region_name=region_name or os.environ.get("AWS_REGION"))
    s3 = session.client("s3")
    s3.upload_file(str(path), bucket, key)
    return {"bucket": bucket, "key": key, "source": str(path)}


def archive_directory(directory_path, bucket_name=None, prefix="", region_name=None):
    directory = Path(directory_path)
    if not directory.is_dir():
        raise NotADirectoryError(directory_path)

    archived = []
    for item in sorted(directory.iterdir()):
        if item.is_file():
            key = f"{prefix.rstrip('/') + '/' if prefix else ''}{item.name}"
            archived.append(archive_metric_snapshot(item, bucket_name=bucket_name, object_key=key, region_name=region_name))
    return archived


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Archive exported metric snapshots to Amazon S3")
    parser.add_argument("path")
    parser.add_argument("--bucket", default=os.environ.get("AWS_S3_BUCKET"))
    parser.add_argument("--key")
    parser.add_argument("--prefix", default="")
    parser.add_argument("--region", default=os.environ.get("AWS_REGION"))
    args = parser.parse_args()

    target = Path(args.path)
    if target.is_dir():
        result = archive_directory(target, bucket_name=args.bucket, prefix=args.prefix, region_name=args.region)
    else:
        result = archive_metric_snapshot(target, bucket_name=args.bucket, object_key=args.key, region_name=args.region)
    print(result)
