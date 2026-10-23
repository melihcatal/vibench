import boto3

def compare_metric_series(metric_name, dimension_name, dimension_values, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    metric_queries = [
        {
            'Id': f'm{i+1}',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/EC2',
                    'MetricName': metric_name,
                    'Dimensions': {dimension_name: value}
                },
                'Period': 300,
                'Stat': 'Average'
            }
        }
        for i, value in enumerate(dimension_values)
    ]
    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=start_time,
        EndTime=end_time
    )
    return response