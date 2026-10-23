import boto3

def compare_metric_series(metric_name, dimension_name, dimension_values, start_time, end_time):
    client = boto3.client('cloudwatch')
    datapoints = {}
    for value in dimension_values:
        response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[{'Name': dimension_name, 'Value': value}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average'])
        datapoints[value] = response['Datapoints']
    return datapoints