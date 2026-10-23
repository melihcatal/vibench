import boto3

class LoginAuditStore:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def store_audit_record(self, audit_record):
        self.table.put_item(Item=audit_record)

    def get_audit_record(self, audit_id):
        response = self.table.get_item(Key={'id': audit_id})
        return response.get('Item')

    def delete_audit_record(self, audit_id):
        self.table.delete_item(Key={'id': audit_id})