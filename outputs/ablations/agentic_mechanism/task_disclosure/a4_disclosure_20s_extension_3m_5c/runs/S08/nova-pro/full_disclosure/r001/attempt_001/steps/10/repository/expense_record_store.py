import boto3

class ExpenseRecordStore:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb', region_name='us-west-2')
        self.table_name = 'ExpenseRecords'

    def put_expense_record(self, expense_record):
        response = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=expense_record
        )
        return response

    def get_expense_record(self, expense_id):
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key={'ExpenseID': {'S': expense_id}}
        )
        return response.get('Item', None)

    def delete_expense_record(self, expense_id):
        response = self.dynamodb.delete_item(
            TableName=self.table_name,
            Key={'ExpenseID': {'S': expense_id}}
        )
        return response