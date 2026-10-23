import boto3

def persist_audit_record(audit_record):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FederatedLoginAudit')
    table.put_item(Item=audit_record)

if __name__ == '__main__':
    audit_record = {
        'id': '1234567890',
        'timestamp': '2022-01-01T12:00:00Z',
        'status': 'success',
        'user_id': 'user123'
    }
    persist_audit_record(audit_record)