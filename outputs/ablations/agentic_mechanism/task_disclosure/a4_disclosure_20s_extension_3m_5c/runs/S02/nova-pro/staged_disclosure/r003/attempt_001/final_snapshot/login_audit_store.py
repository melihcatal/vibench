import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('FederatedLoginAudit')

def store_audit_record(record):
    table.put_item(Item=record)

# Example usage:
# store_audit_record({
#     'user_id': 'user123',
#     'login_time': '2026-09-20T12:00:00Z',
#     'provider': 'Google',
#     'status': 'success'
# })