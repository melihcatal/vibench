import boto3

def summarize_audit_events():
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        Namespace='AWS/Cognito',
        MetricName='UserPoolSignIns',
        Dimensions=[{'Name': 'UserPoolId', 'Value': 'YOUR_USER_POOL_ID'}],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        EndTime=datetime.datetime.utcnow(),
        Period=3600,
        Statistics=['Sum']
    )
    print(response)