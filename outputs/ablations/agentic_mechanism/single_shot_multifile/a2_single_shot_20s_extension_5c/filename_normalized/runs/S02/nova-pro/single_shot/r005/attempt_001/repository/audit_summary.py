import boto3
from botocore.exceptions import ClientError

def summarize_audit_events(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        response = table.scan()
        events = response['Items']
        summary = {'total_events': len(events)}
        for event in events:
            if 'error' in event:
                summary['errors'] = summary.get('errors', 0) + 1
        return summary
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None