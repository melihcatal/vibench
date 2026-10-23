import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")

table_name = "ManagedNoSQLStore"


def conditional_update(primary_id, update_expression, expression_attribute_values):
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key={"id": primary_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW",
    )
    return response.get("Attributes", None)
