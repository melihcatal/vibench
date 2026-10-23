import os

import boto3


def archive_record_snapshot(bucket_name, key, body, content_type="application/json"):
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=body
        if isinstance(body, (bytes, bytearray))
        else str(body).encode("utf-8"),
        ContentType=content_type,
    )
    return {"bucket": bucket_name, "key": key, "archived": True}


def main():
    return archive_record_snapshot(
        os.environ["ARCHIVE_BUCKET"],
        os.environ["ARCHIVE_KEY"],
        os.environ.get("ARCHIVE_BODY", "{}"),
    )
