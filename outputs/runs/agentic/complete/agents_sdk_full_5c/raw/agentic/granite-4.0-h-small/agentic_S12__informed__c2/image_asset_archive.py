import os
import json
import boto3
from typing import List, Dict

def archive_analysis(analysis_id: str, labels: List[str], caption: str, text: List[str], unsafe: bool, s3_bucket: str, s3_prefix: str = "image-analysis"):
    s3 = boto3.client('s3')
    archive_key = f"{s3_prefix}/{analysis_id}.json"
    payload = {
        "analysis_id": analysis_id,
        "labels": labels,
        "caption": caption,
        "text_segments": text,
        "unsafe_content": unsafe
    }
    s3.put_object(Body=json.dumps(payload), Bucket=s3_bucket, Key=archive_key)
