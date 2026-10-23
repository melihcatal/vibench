import boto3

dynamodb = boto3.resource('dynamodb')

def store_audit_record(record):
    table = dynamodb.Table('FederatedLoginAudit')
    table.put_item(Item=record)

if __name__ == '__main__':
    audit_record = {
        'audit_id': '1234567890',
        'user_id': 'user123',
        'timestamp': '2026-09-20T12:34:56Z',
        'event': 'login'
    }
    store_audit_record(audit_record)