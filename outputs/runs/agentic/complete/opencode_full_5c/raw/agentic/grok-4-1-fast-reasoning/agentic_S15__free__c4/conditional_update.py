import boto3
from boto3.dynamodb.conditions import Attr
from database_client import DYNAMODB_TABLE_NAME, AWS_REGION
from database_models import Document, UpdateResponse


def conditional_update(
    doc_id: str, updates: Document, current_version: int
) -> UpdateResponse:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    expression_names = {f"#{k}": k for k in updates}
    expression_values = {f":v{k}": updates[k] for k in updates}
    expression_values[":one"] = 1
    expression_values[":ver"] = current_version
    set_parts = [f"#{k} = :v{k}" for k in updates]
    update_expression = "SET " + ", ".join(set_parts) + ", version = version + :one"
    try:
        table.update_item(
            Key={"id": doc_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ConditionExpression=Attr("version").eq(":ver"),
        )
        return {"status": "success", "doc_id": doc_id}
    except Exception:
        return {"status": "failed"}
