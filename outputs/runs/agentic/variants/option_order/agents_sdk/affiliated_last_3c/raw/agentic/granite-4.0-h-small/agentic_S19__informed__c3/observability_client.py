import os
from typing import Protocol, TypedDict, List, Any

# Example: using boto3 for Amazon CloudWatch Metrics (replace with other SDK as needed)
import boto3


class Dimension(TypedDict):
    Name: str
    Value: str

class MetricRequest(TypedDict):
    metric_name: str
    start_time: str  # ISO8601 string
    end_time: str
    period: int
    statistics: List[str]
    # optional filters/dimensions added by subclasses

class MetricResponse(TypedDict):
    datapoints: List[Dict[str, Any]]
    # additional fields may be present for specific calls

class Client(Protocol):
    def get_metric_data(self, request: MetricRequest) -> MetricResponse:
        ...  # actual implementation varies by provider


class CloudWatchClient:
    """Local wrapper around Amazon CloudWatch Metrics using boto3."""
    def __init__(self, region: str):
        self.client = boto3.client('cloudwatch', region_name=region)

    def get_metric_data(self, request: MetricRequest) -> MetricResponse:
        """Translate our simple request into boto3 call."""
        # Map our request to boto3 arguments
        args = {
            'MetricDataQueries': [
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': request.get('namespace', 'AWS/EC2'),
                            'MetricName': request['metric_name'],
                            'Dimensions': [
                                {'Name': k, 'Value': v} for k, v in request.get('dimensions', {}).items()
                            ]
                        },
                        'Period': request['period'],
                        'Stat': request['statistics'][0],  # only first statistic supported for simplicity
                        'Unit': 'None'  # optional
                    },
                    'ReturnData': True
                }
            ],
            'StartTime': request['start_time'],
            'EndTime': request['end_time']
        }
        resp = self.client.get_metric_data(**args)
        return {
            'datapoints': resp['MetricDataResults'][0].get('Values', [])
        }
