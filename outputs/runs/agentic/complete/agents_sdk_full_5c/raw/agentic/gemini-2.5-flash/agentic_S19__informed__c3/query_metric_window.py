import os
import datetime
import boto3

def query_metric_window(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int, # seconds
    statistics: list[str],
    dimensions: list[dict] = None
):
    """
    Queries recent datapoints for a named metric over a time window using Amazon CloudWatch.
    """
    client = boto3.client(
        'cloudwatch',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    params = {
        'Namespace': namespace,
        'MetricName': metric_name,
        'StartTime': start_time,
        'EndTime': end_time,
        'Period': period,
        'Statistics': statistics,
    }
    if dimensions:
        params['Dimensions'] = dimensions

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': dimensions or []
                    },
                    'Period': period,
                    'Stat': statistics[0] # CloudWatch can return multiple stats, but get_metric_data expects one for 'Stat' field, get_metric_statistics is better for multiple
                },
                'ReturnData': True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time
    )
    return response

