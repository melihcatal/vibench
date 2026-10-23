import boto3

dynamodb = boto3.resource('dynamodb')

def store_audit_record(record):
    table = dynamodb.Table('FederatedLoginAudit')
    table.put_item(Item=record)

if __name__ == '__main__':
    # Example usage
    audit_record = {
        'id': '12345',
        'timestamp': '2026-09-20T00:00:00Z',
        'user_id': 'user123',
        'event': 'login',
        'details': 'Successful login'
    }
    store_audit_record(audit_record)