from typing import Dict, List, Optional
import os
import boto3
from datetime import datetime
import json


class MetricsExportArchiver:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )
        self.bucket_name = os.getenv("METRICS_ARCHIVE_BUCKET_NAME")

    def archive_metrics_export(self, export_data: Dict, export_name: str) -> str:
        timestamp = datetime.utcnow().isoformat()
        key = f"metrics_exports/{export_name}_{timestamp}.json"

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(export_data),
            ContentType="application/json",
        )
        return f"s3://{self.bucket_name}/{key}"
