from typing import Dict, List, Optional
import os
import boto3
from datetime import datetime, timedelta


class CloudWatchMetricsClient:
    def __init__(self):
        self.client = boto3.client(
            "cloudwatch",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def query_metric_window(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        dimensions: Optional[List[Dict[str, str]]] = None,
    ) -> List[Dict]:
        response = self.client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions or [],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["SampleCount", "Average", "Sum", "Minimum", "Maximum"],
        )
        return response.get("Datapoints", [])
