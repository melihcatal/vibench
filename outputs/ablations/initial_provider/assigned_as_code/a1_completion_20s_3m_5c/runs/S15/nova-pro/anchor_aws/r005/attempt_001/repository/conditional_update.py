import boto3

from database_models import normalize_document


def conditional_update(id, update_payload, config):
    table = boto3.resource("dynamodb", region_name=config["region"]).Table(config["table_name"])
    update_expression = "set #" + config["update_field"] + " = :value"
    expression_attribute_values = {":" + config["update_field"]: update_payload[config["update_field"]]}
    expression_attribute_names = { "#" + config["update_field"]: config["update_field"]}
    response = table.update_item(
        Key={config["key_field"]: id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names,
        ReturnValues="ALL_NEW"
    )
    item = response.get("Attributes")
    if item:
        return normalize_document(item)
    return None