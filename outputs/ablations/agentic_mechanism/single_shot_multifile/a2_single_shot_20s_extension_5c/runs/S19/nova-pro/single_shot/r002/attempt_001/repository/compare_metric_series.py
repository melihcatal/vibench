import boto3

def compare_metric_series(metric_name, start_time, end_time, dimension_name, dimension_values):
    client = boto3.client('cloudwatch')
    metric_queries = [
        {
            'Id': f'm{i}',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/EC2',
                    'MetricName': metric_name,
                    'Dimensions': [{
                        'Name': dimension_name,
                        'Value': value
                    }]
                },
                'Period': 300,
                'Stat': 'Average'
            }
        } for i, value in enumerate(dimension_values, 1)
    ]
    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=start_time,
        EndTime=end_time
    )
    return [result['Values'] for result in response['MetricDataResults']]