import boto3

def compare_metric_series(namespace, metric_name, resource1, resource2, dimension_name=None, start_time=None, end_time=None):
    cloudwatch = boto3.client('cloudwatch')
    
    metric_data_queries = [
        {
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': [{'Name': dimension_name, 'Value': resource1}] if dimension_name else []
                },
                'Period': 300,
                'Stat': 'Average'
            }
        },
        {
            'Id': 'm2',
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': [{'Name': dimension_name, 'Value': resource2}] if dimension_name else []
                },
                'Period': 300,
                'Stat': 'Average'
            }
        }
    ]
    
    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=start_time,
        EndTime=end_time
    )
    
    return response['MetricDataResults']