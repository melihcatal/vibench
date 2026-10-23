from typing import Dict, Any
import os
import boto3
from botocore.exceptions import NoCredentialsError


class RecordExporter:
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.bucket_name = os.getenv("S3_BUCKET_NAME", "document-archives")

    def export_to_archive(self, document_id: str, document_data: Dict[str, Any]) -> str:
        import json

        file_key = f"archives/{document_id}.json"
        self.s3_client.put_object(
            Bucket=self.bucket_name, Key=file_key, Body=json.dumps(document_data)
        )
        return f"s3://{self.bucket_name}/{file_key}"
