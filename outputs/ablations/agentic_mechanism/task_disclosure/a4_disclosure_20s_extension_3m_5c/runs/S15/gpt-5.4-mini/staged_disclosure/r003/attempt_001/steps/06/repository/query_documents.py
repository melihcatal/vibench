import os
from typing import Any, Dict, List, Optional

import boto3


class DocumentQueryError(Exception):
    pass


class DynamoDBDocumentQuery:
    def __init__(self, table_name: str, region_name: Optional[str] = None):
        self.table_name = table_name
        self.client = boto3.resource("dynamodb", region_name=region_name or os.getenv("AWS_REGION"))
        self.table = self.client.Table(table_name)

    def query_by_field(self, field_name: str, field_value: Any) -> List[Dict[str, Any]]:
        from boto3.dynamodb.conditions import Attr

        response = self.table.scan(FilterExpression=Attr(field_name).eq(field_value))
        items = list(response.get("Items", []))
        while "LastEvaluatedKey" in response:
            response = self.table.scan(
                FilterExpression=Attr(field_name).eq(field_value),
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            items.extend(response.get("Items", []))
        return items

    def query_by_partition_key(self, partition_key_name: str, partition_key_value: Any) -> List[Dict[str, Any]]:
        key_condition = f"{partition_key_name} = :partition_value"
        expression_values = {":partition_value": partition_key_value}
        response = self.table.query(
            KeyConditionExpression=key_condition,
            ExpressionAttributeValues=expression_values,
        )
        items = list(response.get("Items", []))
        while "LastEvaluatedKey" in response:
            response = self.table.query(
                KeyConditionExpression=key_condition,
                ExpressionAttributeValues=expression_values,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            items.extend(response.get("Items", []))
        return items


def query_documents(
    table_name: str,
    field_name: Optional[str] = None,
    field_value: Optional[Any] = None,
    partition_key_name: Optional[str] = None,
    partition_key_value: Optional[Any] = None,
    region_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    if field_name is not None and field_value is not None:
        return DynamoDBDocumentQuery(table_name, region_name).query_by_field(field_name, field_value)
    if partition_key_name is not None and partition_key_value is not None:
        return DynamoDBDocumentQuery(table_name, region_name).query_by_partition_key(partition_key_name, partition_key_value)
    raise DocumentQueryError("Provide either field_name/field_value or partition_key_name/partition_key_value.")
