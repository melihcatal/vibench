import boto3
import os
from typing import Dict, Any, Optional
from datetime import datetime


class RecordExporter:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "document-exports")

    def export_to_s3(self, document: Dict[str, Any], document_id: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        key = f"exports/{document_id}_{timestamp}.json"
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=str(document),
            ContentType="application/json",
        )
        return f"s3://{self.bucket_name}/{key}"
