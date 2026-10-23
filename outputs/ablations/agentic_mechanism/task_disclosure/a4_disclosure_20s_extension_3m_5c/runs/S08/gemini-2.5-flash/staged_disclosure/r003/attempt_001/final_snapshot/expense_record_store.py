import boto3
import os

class ExpenseRecordStore:
    def __init__(self, table_name=None):
        self.dynamodb = boto3.resource('''dynamodb''',
                                      region_name=os.getenv('''AWS_REGION''', '''us-east-1'''))
        self.table_name = table_name if table_name else os.getenv('''DYNAMODB_TABLE_NAME''', '''ExpenseRecords''')
        self.table = self.dynamodb.Table(self.table_name)

    def persist_record(self, record: dict):
        '''
        Persists a normalized expense record to DynamoDB.
        The record dictionary should contain item attributes.
        '''
        try:
            response = self.table.put_item(Item=record)
            return response
        except Exception as e:
            print(f"Error persisting record to DynamoDB: {e}")
            raise

