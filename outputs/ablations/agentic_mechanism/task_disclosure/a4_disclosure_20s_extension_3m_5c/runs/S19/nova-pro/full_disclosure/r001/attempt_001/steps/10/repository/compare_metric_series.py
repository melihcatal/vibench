import boto3

def compare_metric_series(namespace, metric_name, dimension_name, resource_id_1, resource_id_2, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    
    response_1 = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': dimension_name,
            'Value': resource_id_1
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    
    response_2 = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': dimension_name,
            'Value': resource_id_2
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    
    if response_1['Datapoints'] and response_2['Datapoints']:
        print(f'Metric values for {resource_id_1} and {resource_id_2} over the specified window:')
        for datapoint_1, datapoint_2 in zip(response_1['Datapoints'], response_2['Datapoints']):
            print(f'Timestamp: {datapoint_1['Timestamp']}, {resource_id_1}: {datapoint_1['Average']}, {resource_id_2}: {datapoint_2['Average']}')
    else:
        print('No datapoints found for one or both resources.')