import boto3


def query_documents(
    table_name, index_name, key_condition_expression, expression_attribute_values
):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    response = table.query(
        IndexName=index_name,
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
    return response.get("Items", [])


if __name__ == "__main__":
    print(
        query_documents(
            "example-table",
            "example-index",
            "example-key = :example-value",
            {":example-value": "example-value"},
        )
    )
