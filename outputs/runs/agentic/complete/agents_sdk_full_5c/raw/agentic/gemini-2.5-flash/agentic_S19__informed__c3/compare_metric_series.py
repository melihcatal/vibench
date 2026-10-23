import os
import datetime
import boto3

def compare_metric_series(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int, # seconds
    statistics: list[str],
    dimensions_series_1: list[dict],
    dimensions_series_2: list[dict]
):
    """
    Compares metric values for two resources or dimension filters over the same window
    using Amazon CloudWatch.
    """
    client = boto3.client(
        'cloudwatch',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    metric_data_queries = [
        {
            'Id': 'series_1',
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': dimensions_series_1
                },
                'Period': period,
                'Stat': statistics[0]
            },
            'ReturnData': True,
        },
        {
            'Id': 'series_2',
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': dimensions_series_2
                },
                'Period': period,
                'Stat': statistics[0]
            },
            'ReturnData': True,
        }
    ]

    response = client.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=start_time,
        EndTime=end_time
    )
    return response

