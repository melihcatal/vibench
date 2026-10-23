import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")

table_name = "ManagedNoSQLStore"


def query_documents(field_name, field_value):
    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr(field_name).eq(field_value)
    )
    return response.get("Items", [])
