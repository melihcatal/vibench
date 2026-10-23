from database_client import get_db_client, get_table_name
from database_models import DocumentUpdateRequest
from botocore.exceptions import ClientError
from decimal import Decimal
import json


def conditional_update(
    document_id: str, update_data: DocumentUpdateRequest, current_version: int
):
    dynamodb = get_db_client()
    table_name = get_table_name()
    table = dynamodb.Table(table_name)

    update_expression_parts = []
    expression_attribute_values = {
        ":current_version": current_version,
        ":new_version": current_version + 1,
    }
    expression_attribute_names = {"#v": "version"}

    update_expression_parts.append("#v = :new_version")

    update_dict = json.loads(
        update_data.model_dump_json(exclude_unset=True), parse_float=Decimal
    )

    for key, value in update_dict.items():
        expression_attribute_names[f"#{key}"] = key
        expression_attribute_values[f":{key}"] = value
        update_expression_parts.append(f"#{key} = :{key}")

    update_expression = "SET " + ", ".join(update_expression_parts)

    try:
        response = table.update_item(
            Key={"document_id": document_id},
            UpdateExpression=update_expression,
            ConditionExpression="#v = :current_version",
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        return response
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(
                f"Conditional update failed for document {document_id}: Version mismatch."
            )
            return None
        else:
            raise e
