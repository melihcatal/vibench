import boto3

def store_audit_record(record):
    client = boto3.client('dynamodb')
    client.put_item(
        TableName='LoginAuditTable',
        Item=record
    )

if __name__ == '__main__':
    store_audit_record({})