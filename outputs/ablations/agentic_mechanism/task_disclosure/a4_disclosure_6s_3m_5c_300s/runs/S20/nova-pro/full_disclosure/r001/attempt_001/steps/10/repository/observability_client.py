import boto3

class ObservabilityClient:
    def __init__(self, region_name='us-west-2'):
        self.client = boto3.client('logs', region_name=region_name)

    def get_log_groups(self):
        response = self.client.describe_log_groups()
        return response['logGroups']

    def get_log_events(self, log_group_name, log_stream_name, start_time, end_time):
        response = self.client.filter_log_events(
            logGroupName=log_group_name,
            logStreamNames=[log_stream_name],
            startTime=start_time,
            endTime=end_time
        )
        return response['events']

    def put_log_events(self, log_group_name, log_stream_name, log_events):
        response = self.client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )
        return response