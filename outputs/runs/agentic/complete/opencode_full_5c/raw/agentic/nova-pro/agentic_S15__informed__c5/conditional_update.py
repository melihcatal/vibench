import boto3


def conditional_update(table_name, key, update_expression, expression_attribute_values):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression="attribute_exists(id)",
    )


if __name__ == "__main__":
    conditional_update(
        "my_table", {"id": "123"}, "SET name = :val1", {":val1": "Jane Doe"}
    )
