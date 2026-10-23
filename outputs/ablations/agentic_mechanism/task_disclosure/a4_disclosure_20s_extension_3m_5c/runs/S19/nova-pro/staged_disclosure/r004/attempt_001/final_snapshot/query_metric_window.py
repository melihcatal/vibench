import boto3

def query_metric_window(metric_name, start_time, end_time, namespace='AWS/CloudWatch'):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
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

# Example usage:
# response = query_metric_window('CPUUtilization', '2026-09-15T00:00:00Z', '2026-09-20T00:00:00Z')