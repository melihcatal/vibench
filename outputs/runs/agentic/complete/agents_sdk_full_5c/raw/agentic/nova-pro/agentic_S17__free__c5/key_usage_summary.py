import boto3

def get_key_usage_summary(key_id):
    cloudwatch_client = boto3.client('cloudwatch')
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/KMS',
        MetricName='EncryptDecryptBytes',
        Dimensions=[{'Name': 'KeyId', 'Value': key_id}],
        StartTime='2023-01-01T00:00:00Z',
        EndTime='2023-01-02T00:00:00Z',
        Period=86400,
        Statistics=['Sum']
    )
    return response