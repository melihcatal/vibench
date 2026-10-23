import os
from typing import BinaryIO, Union

import boto3


def upload_object(bucket: str, key: str, data: Union[str, bytes, bytearray, BinaryIO], content_type: str | None = None) -> str:
    s3 = boto3.client("s3")
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    if isinstance(data, str):
        s3.upload_file(data, bucket, key, ExtraArgs=extra_args or None)
    else:
        body = data if isinstance(data, (bytes, bytearray)) else data.read()
        s3.put_object(Bucket=bucket, Key=key, Body=body, **extra_args)

    return f"s3://{bucket}/{key}"


def main() -> None:
    bucket = os.environ["AWS_S3_BUCKET"]
    key = os.environ["AWS_S3_KEY"]
    path = os.environ.get("AWS_S3_FILE_PATH")
    payload = path if path else os.environ["AWS_S3_BYTES"].encode()
    upload_object(bucket, key, payload)


if __name__ == "__main__":
    main()
