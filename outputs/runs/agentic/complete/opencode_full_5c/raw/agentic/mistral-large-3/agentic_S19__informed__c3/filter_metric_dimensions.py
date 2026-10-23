from typing import Dict, List, Optional
import os
import boto3
from datetime import datetime, timedelta


class CloudWatchMetricsFilter:
    def __init__(self):
        self.client = boto3.client(
            "cloudwatch",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def filter_metric_dimensions(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        dimensions: List[Dict[str, str]],
    ) -> List[Dict]:
        response = self.client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["SampleCount", "Average", "Sum", "Minimum", "Maximum"],
        )
        return response.get("Datapoints", [])
