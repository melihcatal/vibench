import boto3
from typing import Dict, List, Optional
from datetime import datetime

class ObservabilityClient:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')

    def get_metric_data(self, metric_name: str, namespace: str, start_time: datetime, end_time: datetime, period: int, statistics: List[str], dimensions: Optional[Dict[str, str]] = None) -> List[Dict]:
        metric_dimensions = []
        if dimensions:
            for name, value in dimensions.items():
                metric_dimensions.append({'Name': name, 'Value': value})

        response = self.cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=statistics,
            Dimensions=metric_dimensions
        )
        return response.get('Datapoints', [])

    def get_metric_widget_image(self, metric_widget_json: str) -> bytes:
        response = self.cloudwatch.get_metric_widget_image(
            MetricWidget=metric_widget_json
        )
        return response.get('MetricWidgetImage')
