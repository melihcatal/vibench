from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError
from database_client import get_dynamodb_table

def conditional_update(document_id: str, update_data: Dict[str, Any], current_version: int) -> bool:
    table = get_dynamodb_table()
    
    update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in update_data.keys())
    expression_attribute_names = {f"#{k}": k for k in update_data.keys()}
    expression_attribute_values = {f":{k}": v for k, v in update_data.items()}
    
    try:
        response = table.update_item(
            Key={"id": document_id},
            UpdateExpression=update_expression,
            ConditionExpression="#v = :current_version",
            ExpressionAttributeNames={"#v": "version"} | expression_attribute_names,
            ExpressionAttributeValues={":current_version": current_version} | expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return False
        raise