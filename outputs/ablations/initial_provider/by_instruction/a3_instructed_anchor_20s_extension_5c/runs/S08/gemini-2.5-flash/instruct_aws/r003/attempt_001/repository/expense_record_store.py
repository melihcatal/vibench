import boto3
import os
import json

def persist_expense_record(record: dict, table_name: str = 'ExpenseRecords') -> dict:
    """
    Persists normalized expense records in AWS DynamoDB.
    """
    # Instantiate a DynamoDB client
    # Ensure AWS credentials are configured (e.g., via environment variables, ~/.aws/credentials)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # Specify a region
    table = dynamodb.Table(table_name)

    try:
        # DynamoDB requires all non-key attributes to be non-empty strings, numbers, or booleans.
        # Empty strings or lists/dicts containing empty strings are not allowed.
        # Convert dict to JSON string for complex attributes if necessary, or clean it.
        item_to_put = json.loads(json.dumps(record, default=str))
        
        # DynamoDB primary key requires at least one attribute. Assuming 'document_id' as a unique key for now.
        # In a real application, you would ensure a unique ID is generated for each record.
        if "document_id" not in item_to_put:
            import uuid
            item_to_put["document_id"] = str(uuid.uuid4())

        response = table.put_item(Item=item_to_put)
        return {"status": "success", "record_id": item_to_put["document_id"], "dynamodb_response": response}
    except Exception as e:
        return {"status": "error", "message": f"Error persisting record to DynamoDB: {e}"}
