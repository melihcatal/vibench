import boto3
from datetime import datetime
from typing import List, Dict
from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint

def query_metric_window(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    namespace: str = 'AWS/EC2',
    period: int = 300,
    region: str = None
) -> List[MetricDatapoint]:
    client = get_cloudwatch_client(region)
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name
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
