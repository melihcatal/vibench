
import boto3
import os
import json

class ExpenseRecordStore:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.environ.get('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        self.table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'ExpenseRecords')
        self.table = self.dynamodb.Table(self.table_name)

    def save_expense_record(self, record: dict):
        try:
            # DynamoDB requires all values to be non-empty strings, numbers, or binary
            # Convert dict to JSON string for storage if it contains nested structures
            # or if any value might be empty (DynamoDB does not allow empty strings)
            item = json.loads(json.dumps(record))
            self.table.put_item(Item=item)
            return {"status": "success", "message": f"Record saved to {self.table_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

