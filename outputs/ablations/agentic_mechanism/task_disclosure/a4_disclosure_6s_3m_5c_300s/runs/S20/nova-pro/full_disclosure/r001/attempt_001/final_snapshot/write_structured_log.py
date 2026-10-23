import boto3

def write_structured_log(log_group_name, log_stream_name, log_events):
    cloudwatch_logs = boto3.client('logs')
    response = cloudwatch_logs.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events
    )
    return response

# Example usage
# log_group_name = 'my-log-group'
# log_stream_name = 'my-log-stream'
# log_events = [
#     {
#         'timestamp': int(time.time() * 1000),
#         'message': 'Example log message'
#     }
# ]
# response = write_structured_log(log_group_name, log_stream_name, log_events)
# print(response)