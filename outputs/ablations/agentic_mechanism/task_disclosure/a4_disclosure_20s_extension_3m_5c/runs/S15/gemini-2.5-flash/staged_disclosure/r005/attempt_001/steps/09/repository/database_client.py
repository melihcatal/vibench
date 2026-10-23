import boto3
import os

class DatabaseClient:
    def __init__(self, region_name=None):
        if region_name is None:
            region_name = os.environ.get("AWS_REGION", "us-east-1") # Default region

        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.client = boto3.client("dynamodb", region_name=region_name)

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
