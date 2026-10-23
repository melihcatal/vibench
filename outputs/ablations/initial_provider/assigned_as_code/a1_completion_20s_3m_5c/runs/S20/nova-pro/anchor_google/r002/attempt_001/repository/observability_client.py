import boto3

cw_logs = boto3.client('logs', region_name='us-west-2')

def get_cw_logs_client():
    return cw_logs

def normalize_log_event(log_event):
    return {
        'timestamp': log_event['timestamp'],
        'message': log_event['message'],
        'correlation_id': log_event.get('correlation_id', '')
    }

def parse_query_results(query_results):
    return [result['@message']['value'] for result in query_results]