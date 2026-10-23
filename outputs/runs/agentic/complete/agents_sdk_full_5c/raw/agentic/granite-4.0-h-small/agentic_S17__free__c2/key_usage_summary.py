import boto3
import os
from botocore.exceptions import ClientError
from datetime import datetime
from typing import Dict, List, Any

# Use CloudWatch Logs Insights to summarize KMS key usage
logs_client = boto3.client('logs')

# Environment variable for KMS key ARN to monitor
KMS_KEY_ARN = os.getenv('KMS_KEY_ARN', 'arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678-901234567890')


def key_usage_summary(days: int = 30) -> Dict[str, Any]:
    """Return a summary of KMS key usage and recent events for the past `days` days."""
    try:
        # Build query that counts Decrypt and Encrypt events per day
        query = f'''
            fields @timestamp, @message
            | filter @message like /%kms.amazonaws.com%/ and @message like /%KeyId=%s%/ \
              and (@message like /%Decrypt%/ or @message like /%Encrypt%/)
            | parse @message /KeyId=(?<key_id>\S+)/
            | parse @message /(Decrypt|Encrypt)/ as operation
            | timeseries @timestamp, bin(1d), count(*) as count by operation
        ''' % KMS_KEY_ARN.replace(':', '\:')

        response = logs_client.start_query(
            logGroupName='/aws/kms',
            startTime=int((datetime.utcnow() - datetime.timedelta(days=days)).timestamp()),
            endTime=int(datetime.utcnow().timestamp()),
            queryString=query
        )
        query_id = response['queryId']
        # Poll until results are ready
        while True:
            status = logs_client.get_query_results(queryId=query_id)['status']
            if status == 'Complete':
                break
            elif status == 'Failed':
                raise RuntimeError('Log query failed')
            else:
                # brief sleep to avoid tight loop
                import time
                time.sleep(1)
        results = logs_client.get_query_results(queryId=query_id)['results']
        summary = {'days': days, 'key_id': KMS_KEY_ARN, 'usage': []}
        for rec in results:
            label = rec.get('field', '')
            count = int(rec.get('value', 0))
            if label.startswith('operations:'):
                operation = label.split(':', 1)[1].strip()
                summary['usage'].append({'operation': operation, 'count': count})
        # Add last event timestamp
        logs = logs_client.filter_log_events(
            logGroupName='/aws/kms',
            startTime=int((datetime.utcnow() - datetime.timedelta(days=days)).timestamp()),
            endTime=int(datetime.utcnow().timestamp()),
            filterPattern='%s' % KMS_KEY_ARN.replace(':', '\:')
        )
        last_ts = max(int(ev['timestamp']) for ev in logs['events']) if logs['events'] else None
        summary['last_used'] = datetime.fromtimestamp(last_ts).isoformat() if last_ts else None
        return summary
    except ClientError as exc:
        raise RuntimeError(f'AWS Logs or KMS error: {exc}')

if __name__ == '__main__':
    print(key_usage_summary())
