import io
import os
from typing import BinaryIO, Union

import boto3


def upload_object(
    bucket_name: str,
    object_key: str,
    data: Union[bytes, bytearray, BinaryIO],
    *,
    content_type: str | None = None,
    region_name: str | None = None,
) -> dict:
    s3 = boto3.client("s3", region_name=region_name)
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    if isinstance(data, (bytes, bytearray)):
        body = io.BytesIO(bytes(data))
    else:
        body = data

    response = s3.upload_fileobj(body, bucket_name, object_key, ExtraArgs=extra_args or None)
    return {
        "bucket": bucket_name,
        "key": object_key,
        "provider": "amazon-s3",
        "response": response,
    }


def upload_path(
    bucket_name: str,
    object_key: str,
    file_path: str,
    *,
    content_type: str | None = None,
    region_name: str | None = None,
) -> dict:
    with open(file_path, "rb") as f:
        return upload_object(
            bucket_name,
            object_key,
            f,
            content_type=content_type,
            region_name=region_name,
        )


def main() -> None:
    bucket_name = os.environ["S3_BUCKET_NAME"]
    object_key = os.environ["S3_OBJECT_KEY"]
    file_path = os.environ.get("S3_FILE_PATH")
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    content_type = os.environ.get("S3_CONTENT_TYPE")

    if file_path:
        result = upload_path(
            bucket_name,
            object_key,
            file_path,
            content_type=content_type,
            region_name=region_name,
        )
    else:
        payload = os.environ.get("S3_PAYLOAD", "").encode("utf-8")
        result = upload_object(
            bucket_name,
            object_key,
            payload,
            content_type=content_type,
            region_name=region_name,
        )

    print(result)


if __name__ == "__main__":
    main()
