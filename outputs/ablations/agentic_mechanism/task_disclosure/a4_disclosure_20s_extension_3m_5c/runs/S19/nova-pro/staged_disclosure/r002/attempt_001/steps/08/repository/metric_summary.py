import boto3

# Initialize a session using your AWS credentials
session = boto3.Session(
    aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY',
    region_name='us-west-2'
)

# Create a CloudWatch client
cloudwatch = session.client('cloudwatch')

# Define the metric and namespace
metric_name = 'CPUUtilization'
namespace = 'AWS/EC2'

# Fetch recent metric data
response = cloudwatch.get_metric_statistics(
    Namespace=namespace,
    MetricName=metric_name,
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-0123456789abcdef0'
        }
    ],
    StartTime=(datetime.datetime.utcnow() - datetime.timedelta(days=1)),
    EndTime=datetime.datetime.utcnow(),
    Period=300,
    Statistics=['Average']
)

# Summarize the metric data
print('Recent metric trends or anomalies:')
for datapoint in response['Datapoints']:
    print(f'Timestamp: {datapoint['Timestamp']}, Average: {datapoint['Average']}')