import boto3
from botocore.exceptions import ClientError

# Configuration settings
DYNAMODB_TABLE_NAME = 'YourDynamoDBTableName'
DYNAMODB_REGION_NAME = 'your-region-name'

# DynamoDB client
dynamodb_client = boto3.client('dynamodb', region_name=DYNAMODB_REGION_NAME)

class DynamoDBClient:
    def __init__(self):
        self.table_name = DYNAMODB_TABLE_NAME
        self.client = dynamodb_client

    def get_item(self, key):
        try:
            response = self.client.get_item(
                TableName=self.table_name,
                Key=key
            )
            return response.get('Item')
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    def put_item(self, item):
        try:
            response = self.client.put_item(
                TableName=self.table_name,
                Item=item
            )
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    def update_item(self, key, update_expression, expression_attribute_values):
        try:
            response = self.client.update_item(
                TableName=self.table_name,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues='UPDATED_NEW'
            )
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    def delete_item(self, key):
        try:
            response = self.client.delete_item(
                TableName=self.table_name,
                Key=key
            )
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None