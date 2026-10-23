import boto3

def summarize_error_logs(log_events):
    client = boto3.client('logs', region_name='us-east-1')
    summary = {
        'total_errors': len(log_events),
        'error_messages': [log_event['message'] for log_event in log_events]
    }
    return summary