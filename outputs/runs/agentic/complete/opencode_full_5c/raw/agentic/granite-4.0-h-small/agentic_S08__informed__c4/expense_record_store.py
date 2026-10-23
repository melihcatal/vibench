import os
import json
import boto3
from pathlib import Path
from normalize_expense import normalize_expense

# AWS DynamoDB credentials (replace with real secrets in production)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
region = "us-east-1"

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=region,
)

table_name = "ExpenseRecords"

# Ensure the table exists (simplified - in production you would create it once)
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"}  # Partition key
        ],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
except dynamodb.meta.client.exceptions.ResourceInUseException:
    table = dynamodb.Table(table_name)


def store_expense(normalized: dict) -> None:
    """
    Persist a normalized expense record in Amazon DynamoDB.
    The function expects the output of `normalize_expense` which includes an 'id' field.
    """
    if "id" not in normalized:
        raise ValueError(
            'Normalized document must contain a unique "id" field for DynamoDB'
        )
    # Simplify attributes: only keep scalar fields for demo
    item = {
        "id": normalized["id"],
        "type": normalized["type"],
        "vendor": normalized.get("vendor"),
        "merchant": normalized.get("merchant"),
        "date": normalized["date"],
        "total": normalized["total"],
        "items": json.dumps(normalized.get("items", [])),  # store JSON string
    }
    table.put_item(Item=item)
    print(f"Stored expense record {normalized['id']} into DynamoDB")


# Example local usage (uncomment to test)
# rec = normalize_expense({'vendor':'Acme','date':'2024-07-15','total':125.5,'line_items':[{'desc':'Widget','qty':2,'price':45.0}]})
# rec['id'] = 'e12345'
# store_expense(rec)
