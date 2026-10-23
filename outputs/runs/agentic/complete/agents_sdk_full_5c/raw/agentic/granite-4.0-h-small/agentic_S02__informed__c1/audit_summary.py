import os
import json
from datetime import datetime
from typing import Dict, List
import boto3

# Amazon DynamoDB client for the audit table
DYNAMODB_TABLE = os.getenv('AUDIT_TABLE_NAME')
if not DYNAMODB_TABLE:
    raise RuntimeError('AUDIT_TABLE_NAME environment variable not set')

ddb = boto3.resource('dynamodb')
audit_table = ddb.Table(DYNAMODB_TABLE)

def summarize_audit_events(start_ts: Optional[str] = None, end_ts: Optional[str] = None) -> Dict[str, Any]:
    '''Retrieve audit records for a time window and produce a concise summary.'''
    # DynamoDB Scan with filter expressions for timestamp range
    filter_expr = []
    expression_values = {}
    if start_ts:
        filter_expr.append('timestamp >= :start')
        expression_values[':start'] = int(start_ts)
    if end_ts:
        filter_expr.append('timestamp <= :end')
        expression_values[':end'] = int(end_ts)
    if filter_expr:
        filter_expr = ' and '.join(filter_expr)
    else:
        filter_expr = None
    response = audit_table.scan(FilterExpression=filter_expr, ExpressionAttributeValues=expression_values)
    items = response.get('Items', [])
    summary = {
        'total_events': len(items),
        'events': []
    }
    for evt in items:
        summary['events'].append({
            'event_id': evt.get('event_id'),
            'user_id': evt.get('user_id'),
            'action': evt.get('action'),
            'timestamp': datetime.fromtimestamp(evt.get('timestamp')).isoformat() + 'Z',
            'details': evt.get('details', '{}')
        })
    return summary

if __name__ == '__main__':
    # Simple CLI demo
    import sys
    args = sys.argv[1:]
    start = args[0] if len(args) > 0 else None
    end = args[1] if len(args) > 1 else None
    try:
        summary = summarize_audit_events(start, end)
        print(json.dumps(summary, indent=2))
    except Exception as exc:
        print('Error:', exc)
