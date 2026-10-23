import boto3

def filter_metric_dimensions(metric_name, start_time, end_time, dimension_name, dimension_value):
    client = boto3.client('cloudwatch')
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id':'m1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
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
    return response['MetricDataResults'][0]['Values']