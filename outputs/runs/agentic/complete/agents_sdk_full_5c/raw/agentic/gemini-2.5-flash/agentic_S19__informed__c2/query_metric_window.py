import datetime
from observability_client import get_cloudwatch_client

def query_metric_window(
    metric_name: str,
    namespace: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int = 300, # seconds
    statistic: str = 'Average',
):
    client = get_cloudwatch_client()

    response = client.get_metric_data(
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
    return response

