import boto3
from observability_client import get_cloudwatch_client

cloudwatch = get_cloudwatch_client()

def metric_summary(metric_name, start_time, end_time):
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': metric_name
                    },
                    'Period': 300,
                    'Stat': 'Average'
                }
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )
    return response