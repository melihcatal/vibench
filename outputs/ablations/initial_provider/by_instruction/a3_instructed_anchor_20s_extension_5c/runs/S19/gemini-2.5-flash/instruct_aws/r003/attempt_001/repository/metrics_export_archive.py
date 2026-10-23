import boto3
from typing import Dict, Any

class MetricsArchiver:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def archive_metric_snapshot(self, bucket_name: str, key: str, data: str) -> Dict[str, Any]:
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=data.encode('utf-8') # Ensure data is bytes
            )
            return {"status": "success", "message": f"Metric snapshot archived to s3://{bucket_name}/{key}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
