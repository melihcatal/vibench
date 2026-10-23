import boto3

def filter_metric_dimensions(namespace, metric_name, dimensions):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': dimensions
                    },
                    'Period': 300,
                    'Stat': 'Average'
                }
            }
        ],
        StartTime=boto3.Session().get_config_variable('start_time'),
        EndTime=boto3.Session().get_config_variable('end_time')
    )
    return response
