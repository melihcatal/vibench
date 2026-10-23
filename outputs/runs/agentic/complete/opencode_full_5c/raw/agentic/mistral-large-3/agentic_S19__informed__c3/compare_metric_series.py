from typing import Dict, List, Optional
import os
import boto3
from datetime import datetime, timedelta


class CloudWatchMetricsComparator:
    def __init__(self):
        self.client = boto3.client(
            "cloudwatch",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def compare_metric_series(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        dimensions_a: List[Dict[str, str]],
        dimensions_b: List[Dict[str, str]],
    ) -> Dict:
        response_a = self.client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions_a,
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average", "Sum", "Minimum", "Maximum"],
        )
        response_b = self.client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions_b,
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average", "Sum", "Minimum", "Maximum"],
        )

        datapoints_a = response_a.get("Datapoints", [])
        datapoints_b = response_b.get("Datapoints", [])

        return {
            "series_a": {"dimensions": dimensions_a, "datapoints": datapoints_a},
            "series_b": {"dimensions": dimensions_b, "datapoints": datapoints_b},
        }
