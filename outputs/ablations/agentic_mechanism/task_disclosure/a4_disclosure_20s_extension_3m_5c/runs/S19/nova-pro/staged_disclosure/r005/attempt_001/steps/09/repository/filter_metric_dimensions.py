import boto3

def filter_metric_dimensions(namespace, metric_name, dimension_name, dimension_value):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': [
                            {
                                'Name': dimension_name,
                                'Value': dimension_value
                            }
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Average'
                }
            }
        ],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=60),
        EndTime=datetime.datetime.utcnow()
    )
    return response

if __name__ == '__main__':
    namespace = 'AWS/EC2'
    metric_name = 'CPUUtilization'
    dimension_name = 'InstanceId'
    dimension_value = 'i-1234567890abcdef0'
    response = filter_metric_dimensions(namespace, metric_name, dimension_name, dimension_value)
    print(response)