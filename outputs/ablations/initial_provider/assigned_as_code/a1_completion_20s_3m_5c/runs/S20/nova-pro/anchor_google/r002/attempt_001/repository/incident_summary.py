import boto3
import time

cw_logs = boto3.client('logs', region_name='us-west-2')

def summarize_error_logs(log_group, start_time, end_time):
    results = query_error_logs(log_group, start_time, end_time)
    summary = {
        'total_errors': len(results),
        'error_messages': [result['@message']['value'] for result in results]
    }
    return summary

if __name__ == '__main__':
    log_group = 'my-log-group'
    start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
    end_time = int(time.time() * 1000)
    summary = summarize_error_logs(log_group, start_time, end_time)
    print(summary)