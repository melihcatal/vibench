import boto3
import json
import datetime
from typing import List, Dict, Any


def archive_records(
    records: List[Dict[str, Any]],
    bucket: str,
    key_prefix: str,
    region: str = "us-east-1",
):
    s3 = boto3.client("s3", region_name=region)
    timestamp = datetime.datetime.now().isoformat()
    key = f"{key_prefix}/records_{timestamp}.json"
    content = json.dumps(records, indent=2)
    s3.put_object(Bucket=bucket, Key=key, Body=content, ContentType="application/json")
