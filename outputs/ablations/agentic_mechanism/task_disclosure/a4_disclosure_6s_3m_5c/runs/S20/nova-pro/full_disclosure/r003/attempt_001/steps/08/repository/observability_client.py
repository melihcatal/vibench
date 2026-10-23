import boto3

class ObservabilityClient:
    def __init__(self, region_name='us-west-2'):
        self.client = boto3.client('logs', region_name=region_name)

    def describe_log_groups(self):
        response = self.client.describe_log_groups()
        return response['logGroups']

    def create_log_group(self, log_group_name):
        self.client.create_log_group(logGroupName=log_group_name)

    def describe_log_streams(self, log_group_name):
        response = self.client.describe_log_streams(logGroupName=log_group_name)
        return response['logStreams']

    def create_log_stream(self, log_group_name, log_stream_name):
        self.client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

    def put_log_events(self, log_group_name, log_stream_name, log_events):
        self.client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )

# Example usage:
# client = ObservabilityClient()
# log_groups = client.describe_log_groups()
# print(log_groups)