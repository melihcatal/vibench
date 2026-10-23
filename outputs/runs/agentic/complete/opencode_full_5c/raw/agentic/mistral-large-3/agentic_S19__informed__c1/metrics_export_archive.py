import os
import json
from datetime import datetime
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


class MetricsExporter:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def archive_metric_snapshot(
        self, metric_data: List[Dict], bucket_name: str, prefix: str = "metrics"
    ) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        key = f"{prefix}/metric_snapshot_{timestamp}.json"

        try:
            self.s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=json.dumps(metric_data, indent=2),
                ContentType="application/json",
            )
            return f"s3://{bucket_name}/{key}"
        except ClientError as e:
            return f"Archive error: {str(e)}"

    def archive_metric_snapshots_batch(
        self,
        metric_data_batch: List[List[Dict]],
        bucket_name: str,
        prefix: str = "metrics",
    ) -> List[str]:
        results = []
        for i, metric_data in enumerate(metric_data_batch):
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            key = f"{prefix}/metric_snapshot_{timestamp}_{i}.json"
            try:
                self.s3.put_object(
                    Bucket=bucket_name,
                    Key=key,
                    Body=json.dumps(metric_data, indent=2),
                    ContentType="application/json",
                )
                results.append(f"s3://{bucket_name}/{key}")
            except ClientError as e:
                results.append(f"Archive error: {str(e)}")
        return results

    def get_archived_metric_snapshot(
        self, bucket_name: str, key: str
    ) -> Optional[List[Dict]]:
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=key)
            return json.loads(response["Body"].read().decode("utf-8"))
        except ClientError as e:
            return None
