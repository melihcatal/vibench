import datetime
from observability_client import get_cloudwatch_client

def compare_metric_series(
    metric_name: str,
    namespace: str,
    dimensions_1: dict[str, str],
    dimensions_2: dict[str, str],
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int = 300, # seconds
    statistic: str = 'Average',
):
    client = get_cloudwatch_client()

    cloudwatch_dimensions_1 = [{'Name': k, 'Value': v} for k, v in dimensions_1.items()]
    cloudwatch_dimensions_2 = [{'Name': k, 'Value': v} for k, v in dimensions_2.items()]

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'series1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': cloudwatch_dimensions_1,
                    },
                    'Period': period,
                    'Stat': statistic,
                },
                'ReturnData': True,
            },
            {
                'Id': 'series2',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': cloudwatch_dimensions_2,
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

