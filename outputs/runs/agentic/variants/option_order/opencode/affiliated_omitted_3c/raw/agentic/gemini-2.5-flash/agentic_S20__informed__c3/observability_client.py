import boto3
import os


class CloudWatchLogsClient:
    """Provides a client for interacting with AWS CloudWatch Logs."""

    def __init__(self):
        self.client = boto3.client(
            "logs",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get(
                "AWS_REGION", "us-east-1"
            ),  # Default to us-east-1 if not specified
        )

    def put_log_events(
        self, log_group_name: str, log_stream_name: str, log_events: list
    ):
        """Puts a batch of log events to the specified log stream.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_log_events
        """
        response = self.client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events,
        )
        return response

    def start_query(
        self, log_group_names: list, start_time: int, end_time: int, query_string: str
    ):
        """Starts a CloudWatch Logs Insights query.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.start_query
        """
        response = self.client.start_query(
            logGroupNames=log_group_names,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
        )
        return response

    def get_query_results(self, query_id: str):
        """Retrieves the results of the specified query.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_query_results
        """
        response = self.client.get_query_results(queryId=query_id)
        return response
