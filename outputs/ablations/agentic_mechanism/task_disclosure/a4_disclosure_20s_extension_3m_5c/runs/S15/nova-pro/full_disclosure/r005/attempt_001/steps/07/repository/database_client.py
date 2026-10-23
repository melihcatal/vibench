import boto3

class DynamoDBClient:
    def __init__(self, region_name='us-west-2'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)

    def get_table(self, table_name):
        return self.dynamodb.Table(table_name)

    def create_table(self, table_name, key_schema, attribute_definitions, provisioned_throughput):
        return self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput=provisioned_throughput
        )

    def delete_table(self, table_name):
        table = self.get_table(table_name)
        table.delete()