from database_client import get_table


def query_documents(table_name, field_name, field_value):
    table = get_table(table_name)
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr(field_name).eq(field_value)
    )
    return response.get("Items")
