import boto3

def filter_metric_dimensions(metric_name, dimension_name, dimension_value, start_time, end_time):
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{'Name': dimension_name, 'Value': dimension_value}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'])
    return response['Datapoints']