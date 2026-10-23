import boto3

def compare_metric_series(namespace, metric_name, dimension_name, value1, value2, start_time, end_time):
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
                            'Value': value1
                        }]
                    },
                    'Period': 300,
                    'Stat': 'Average'
                },
                'ReturnData': True
            },
            {
                'Id':'m2',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': [{
                            'Name': dimension_name,
                            'Value': value2
                        }]
                    },
                    'Period': 300,
                    'Stat': 'Average'
                },
                'ReturnData': True
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )
    return response['MetricDataResults']