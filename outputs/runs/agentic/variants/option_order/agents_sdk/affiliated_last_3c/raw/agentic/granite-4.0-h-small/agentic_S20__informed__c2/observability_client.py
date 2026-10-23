import os, json, boto3

class ObservabilityClient:
    """Thin wrapper around Amazon CloudWatch Logs client with common helpers.

    Uses environment variables for configuration:
        - AWS_REGION (default: us-east-1)
        - CLOUDWATCH_LOG_GROUP (default: /my/app/logs)
        - CLOUDWATCH_LOG_STREAM (default: structured-logs)
    """
    def __init__(self, region=None, log_group=None, log_stream=None):
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')
        self.log_group = log_group or os.getenv('CLOUDWATCH_LOG_GROUP', '/my/app/logs')
        self.log_stream = log_stream or os.getenv('CLOUDWATCH_LOG_STREAM', 'structured-logs')
        self.client = boto3.client('logs', region_name=self.region)

    def put_log_events(self, log_data):
        """Write a single structured log entry.

        Args:
            log_data (dict): The log payload (timestamp will be added automatically).
        """
        # CloudWatch requires list of events
        response = self.client.put_log_events(
            logGroupName=self.log_group,
            logStreamName=self.log_stream,
            logEvents=[{
                'timestamp': int(log_data.get('timestamp', time.time()) * 1000),
                'message': json.dumps(log_data)
            }]
        )
        return response

    def query_error_logs(self, severity='ERROR', start_time=None, end_time=None):
        """Query error logs using filter pattern.

        Args:
            severity (str): Severity to filter on.
            start_time (int or datetime): start timestamp (epoch ms).
            end_time (int or datetime): end timestamp (epoch ms).
        """
        if start_time:
            if isinstance(start_time, datetime.datetime):
                start_time = int(start_time.timestamp() * 1000)
            else:
                start_time = int(start_time)
        else:
            start_time = int((datetime.datetime.utcnow() - datetime.timedelta(hours=12)).timestamp() * 1000)
        if end_time:
            if isinstance(end_time, datetime.datetime):
                end_time = int(end_time.timestamp() * 1000)
            else:
                end_time = int(end_time)
        filter_pattern = f"severity={severity}"
        return self.client.filter_log_events(
            logGroupName=self.log_group,
            filterPattern=filter_pattern,
            startTime=start_time,
            endTime=end_time
        )

    def fetch_recent_by_field(self, field, value, duration_minutes=60):
        now_ms = int(datetime.datetime.utcnow().timestamp() * 1000)
        start_ms = now_ms - (duration_minutes * 60 * 1000)
        filter_expr = f"{field}='{value}'"
        return self.client.filter_log_events(
            logGroupName=self.log_group,
            filterPattern=filter_expr,
            startTime=start_ms,
            endTime=now_ms
        )
