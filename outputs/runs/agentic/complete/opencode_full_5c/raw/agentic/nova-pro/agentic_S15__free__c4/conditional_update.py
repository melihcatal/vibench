import boto3


def conditional_update(
    table_name, primary_key, key_value, update_expression, expression_attribute_values
):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key={primary_key: key_value},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW",
    )
    return response.get("Attributes", None)


if __name__ == "__main__":
    print(
        conditional_update(
            "example-table",
            "id",
            "123",
            "set data = :new_data",
            {":new_data": "new example data"},
        )
    )
