import boto3

from database_models import deserialize_document


def conditional_update(document_id, update_expression, expression_attribute_values, config):
    table = boto3.resource("dynamodb", region_name=config["region"]).Table(config["table_name"])
    response = table.update_item(
        Key={config["key_field"]: document_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"
    )
    item = response.get("Attributes")
    if item:
        return deserialize_document(item)
    return None