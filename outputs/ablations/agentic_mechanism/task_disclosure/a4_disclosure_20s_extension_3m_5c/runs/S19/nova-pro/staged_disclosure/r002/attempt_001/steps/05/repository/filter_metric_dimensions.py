import boto3

def query_metric_data(namespace, metric_name, dimensions):
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
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=60),
        EndTime=datetime.datetime.utcnow()
    )
    return response

if __name__ == '__main__':
    namespace = 'AWS/EC2'
    metric_name = 'CPUUtilization'
    dimensions = [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]
    result = query_metric_data(namespace, metric_name, dimensions)
    print(result)