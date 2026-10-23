import boto3

def store_audit_record(record):
    dynamodb = boto3.client('dynamodb')
    table_name = 'FederatedLoginAudit'
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'AuditID': {'S': record['AuditID']},
            'UserID': {'S': record['UserID']},
            'Timestamp': {'S': record['Timestamp']},
            'Provider': {'S': record['Provider']},
            'Status': {'S': record['Status']}
        }
    )

# Example usage
audit_record = {
    'AuditID': 'audit-123',
    'UserID': 'user-456',
    'Timestamp': '2026-09-20T12:34:56Z',
    'Provider': 'Google',
    'Status': 'Success'
}
store_audit_record(audit_record)