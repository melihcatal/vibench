from typing import Any, Dict

import boto3


def archive_export(snapshot: Dict[str, Any], bucket: str, key: str) -> Dict[str, Any]:
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=str(snapshot).encode("utf-8"),
        ContentType="application/json",
    )
    return {"archived": True, "bucket": bucket, "key": key}


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return archive_export(event["snapshot"], event["bucket"], event["key"])
