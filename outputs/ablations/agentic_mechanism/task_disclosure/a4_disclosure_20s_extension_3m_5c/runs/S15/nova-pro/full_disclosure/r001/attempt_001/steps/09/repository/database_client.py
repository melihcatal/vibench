import boto3

DYNAMODB_TABLE_NAME = 'example_table'


class DynamoDBClient:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')

    def get_item(self, key):
        response = self.dynamodb.get_item(
            TableName=DYNAMODB_TABLE_NAME,
            Key=key
        )
        return response.get('Item', None)

    def put_item(self, item):
        response = self.dynamodb.put_item(
            TableName=DYNAMODB_TABLE_NAME,
            Item=item
        )
        return response

    def query(self, key_condition_expression, expression_attribute_values):
        response = self.dynamodb.query(
            TableName=DYNAMODB_TABLE_NAME,
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response.get('Items', [])