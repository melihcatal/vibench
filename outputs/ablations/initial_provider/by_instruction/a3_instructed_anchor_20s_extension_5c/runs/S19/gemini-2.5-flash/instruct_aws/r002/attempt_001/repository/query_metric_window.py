import boto3
import os
from datetime import datetime

def query_metric_window(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300, # 5 minutes
    statistic: str = "Average",
) -> list:
    """
    Queries recent datapoints for a named metric over a time window using AWS CloudWatch.
    """
    cloudwatch = boto3.client('cloudwatch', region_name=os.environ.get("AWS_REGION", "us-east-1"))

    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                    },
                    'Period': period,
                    'Stat': statistic,
                },
                'ReturnData': True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    datapoints = []
    if response and response.get('MetricDataResults'):
        for result in response['MetricDataResults']:
            if result.get('Values') and result.get('Timestamps'):
                for i in range(len(result['Values'])):
                    datapoints.append({
                        'timestamp': result['Timestamps'][i].isoformat(),
                        'value': result['Values'][i]
                    })
    return datapoints
