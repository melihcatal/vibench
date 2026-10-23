import datetime
from observability_client import get_cloudwatch_client

def filter_metric_dimensions(
    metric_name: str,
    namespace: str,
    dimensions: dict[str, str],
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int = 300, # seconds
    statistic: str = 'Average',
):
    client = get_cloudwatch_client()

    # Convert dimensions dict to the format expected by CloudWatch API
    cloudwatch_dimensions = [{'Name': k, 'Value': v} for k, v in dimensions.items()]

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': cloudwatch_dimensions,
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
    return response

