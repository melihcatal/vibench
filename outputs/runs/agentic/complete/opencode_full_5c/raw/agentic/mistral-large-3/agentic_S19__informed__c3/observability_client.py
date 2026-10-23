import os
from typing import Dict, List, Optional
import boto3
from datetime import datetime


class ObservabilityClient:
    def __init__(self):
        self.cloudwatch_client = boto3.client(
            "cloudwatch",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def get_metric_data(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        dimensions: Optional[List[Dict[str, str]]] = None,
    ) -> Dict:
        response = self.cloudwatch_client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions or [],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average", "Sum", "Minimum", "Maximum"],
        )
        return response

    def list_metrics(
        self,
        namespace: str,
        metric_name: Optional[str] = None,
        dimensions: Optional[List[Dict[str, str]]] = None,
    ) -> List[Dict]:
        kwargs = {"Namespace": namespace}
        if metric_name:
            kwargs["MetricName"] = metric_name
        if dimensions:
            kwargs["Dimensions"] = dimensions

        response = self.cloudwatch_client.list_metrics(**kwargs)
        return response.get("Metrics", [])
