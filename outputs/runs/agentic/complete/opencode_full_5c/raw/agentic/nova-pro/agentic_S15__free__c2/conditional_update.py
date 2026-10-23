from database_client import get_table


def conditional_update(
    table_name, document_id, update_expression, expression_attribute_values
):
    table = get_table(table_name)
    response = table.update_item(
        Key={"id": document_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW",
    )
    return response.get("Attributes")
