import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import io
import json
from typing import List
from observability_models import MetricDataPoint

class MetricsExporterArchiver:
    def __init__(self):
        self.s3_client = boto3.client('s3')  # Uses AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
        self.bucket_name = "metrics-archive-bucket"

    def archive_metrics(self, metrics: List[MetricDataPoint], object_prefix: str) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        object_key = f"{object_prefix}/metrics_{timestamp}.json"

        data = [{
            "timestamp": point.timestamp.isoformat(),
            "value": point.value,
            "labels": point.labels
        } for point in metrics]

        json_data = json.dumps(data, indent=2)
        json_bytes = io.BytesIO(json_data.encode('utf-8'))

        self.s3_client.upload_fileobj(
            json_bytes,
            self.bucket_name,
            object_key
        )
        return f"s3://{self.bucket_name}/{object_key}"