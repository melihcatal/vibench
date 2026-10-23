import datetime
import json
from messaging_client import get_cloudwatch_logs_client

def message_summary(log_group_name, message, status, config=None):
    config = config or {}
    logs_client = get_cloudwatch_logs_client(config.get("region"))

    log_stream_name = datetime.datetime.now().strftime("%Y/%m/%d/message_summary")

    log_event = {
        'timestamp': int(round(datetime.datetime.now().timestamp() * 1000)),
        'message': json.dumps({
            "message_id": message.message_id if hasattr(message, 'message_id') else 'N/A',
            "event_type": message.payload.event_type if hasattr(message, 'payload') and hasattr(message.payload, 'event_type') else 'N/A',
            "status": status,
            "data": message.payload.data if hasattr(message, 'payload') and hasattr(message.payload, 'data') else message
        })
    }

    try:
        logs_client.create_log_group(logGroupName=log_group_name)
    except logs_client.exceptions.ResourceAlreadyExistsException:
        pass

    try:
        logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except logs_client.exceptions.ResourceAlreadyExistsException:
        pass

    response = logs_client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[
            log_event
        ]
    )
    return {"next_sequence_token": response["nextSequenceToken"]}
