import boto3
from datetime import datetime
from typing import List
from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint, MetricDimension

def filter_metric_dimensions(
    metric_name: str,
    dimensions: List[MetricDimension],
    start_time: datetime,
    end_time: datetime,
    namespace: str = 'AWS/EC2',
    period: int = 300,
    region: str = None
) -> List[MetricDatapoint]:
    client = get_cloudwatch_client(region)
    metric_dimensions = [{'Name': d.name, 'Value': d.value} for d in dimensions]
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': metric_dimensions
                    },
                    'Period': period,
                    'Stat': 'Average'
                },
                'ReturnData': True
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )
    result = response['MetricDataResults'][0]
    timestamps = result['Timestamps']
    values = result['Values']
    datapoints = [
        MetricDatapoint(timestamp=t, value=v)
        for t, v in zip(timestamps, values)
    ]
    return datapoints
