import os
from typing import BinaryIO, Union

import boto3


def upload_object(bucket: str, key: str, data: Union[str, bytes, BinaryIO]) -> dict:
    s3 = boto3.client("s3")
    if isinstance(data, str):
        with open(data, "rb") as f:
            s3.upload_fileobj(f, bucket, key)
        return {"bucket": bucket, "key": key, "source": data}
    if isinstance(data, bytes):
        import io

        s3.upload_fileobj(io.BytesIO(data), bucket, key)
        return {"bucket": bucket, "key": key, "source": "bytes"}
    s3.upload_fileobj(data, bucket, key)
    return {"bucket": bucket, "key": key, "source": "fileobj"}


def _main() -> None:
    bucket = os.environ["AWS_S3_BUCKET"]
    key = os.environ["AWS_S3_KEY"]
    source = os.environ["AWS_S3_SOURCE"]
    upload_object(bucket, key, source)


if __name__ == "__main__":
    _main()
