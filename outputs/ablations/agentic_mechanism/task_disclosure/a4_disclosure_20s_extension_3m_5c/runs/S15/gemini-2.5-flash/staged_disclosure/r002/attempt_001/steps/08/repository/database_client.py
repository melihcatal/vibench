import os
import boto3

class DynamoDBClient:
    def __init__(self, region_name=None, endpoint_url=None):
        if region_name is None:
            region_name = os.environ.get("AWS_REGION", "us-east-1")
        if endpoint_url is None:
            endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=region_name,
            endpoint_url=endpoint_url
        )

    def get_table(self, table_name):
        return self.dynamodb.Table(table_name)

    def put_item(self, table_name, item):
        table = self.get_table(table_name)
        response = table.put_item(Item=item)
        return response

    def get_item(self, table_name, key):
        table = self.get_table(table_name)
        response = table.get_item(Key=key)
        return response.get("Item")

    def update_item(self, table_name, key, update_expression, expression_attribute_values):
        table = self.get_table(table_name)
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_item(self, table_name, key):
        table = self.get_table(table_name)
        response = table.delete_item(Key=key)
        return response
