import boto3

def filter_metric_dimensions(namespace, metric_name, dimension_name, dimension_value, start_time, end_time):
    client = boto3.client('cloudwatch')
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id':'m1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': [{
                            'Name': dimension_name,
                            'Value': dimension_value
                        }]
                    },
                    'Period': 300,
                    'Stat': 'Average'
                }
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )
    return response['MetricDataResults']