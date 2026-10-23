
import boto3
import os

class ExpenseRecordStore:
    def __init__(self, table_name=None, region_name=None):
        self.table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME", "ExpenseRecords")
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.dynamodb = boto3.resource("dynamodb", region_name=self.region_name)
        self.table = self.dynamodb.Table(self.table_name)

    def persist_record(self, record):
        """
        Persists a normalized expense record to DynamoDB.
        The record should be a dictionary.
        """
        try:
            self.table.put_item(Item=record)
            return {"status": "success", "message": "Record persisted successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

