import boto3

dynamodb = boto3.resource('dynamodb')


class LoginAuditStore:
    def __init__(self, table_name):
        self.table = dynamodb.Table(table_name)

    def persist_audit_record(self, record):
        self.table.put_item(Item=record)

    def get_audit_record(self, record_id):
        response = self.table.get_item(Key={'id': record_id})
        return response.get('Item')

    def list_audit_records(self):
        response = self.table.scan()
        return response.get('Items', [])
