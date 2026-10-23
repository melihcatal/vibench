import boto3

from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class ExpenseRecordStore:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('ExpenseRecords')

    def store_expense_record(self, expense_record):
        try:
            response = self.table.put_item(Item=expense_record)
            return response
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
            return None
        except Exception as e:
            print(f"Error storing expense record: {e}")
            return None

    def get_expense_record(self, record_id):
        try:
            response = self.table.get_item(Key={'id': record_id})
            return response.get('Item')
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
            return None
        except Exception as e:
            print(f"Error retrieving expense record: {e}")
            return None
