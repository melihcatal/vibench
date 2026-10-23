import os
import datetime
import boto3

def filter_metric_dimensions(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int, # seconds
    statistics: list[str],
    dimensions: list[dict]
):
    """
    Queries metric data filtered by resource labels or dimensions using Amazon CloudWatch.
    """
    client = boto3.client(
        'cloudwatch',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'filtered_metric',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': dimensions
                    },
                    'Period': period,
                    'Stat': statistics[0]
                },
                'ReturnData': True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time
    )
    return response

