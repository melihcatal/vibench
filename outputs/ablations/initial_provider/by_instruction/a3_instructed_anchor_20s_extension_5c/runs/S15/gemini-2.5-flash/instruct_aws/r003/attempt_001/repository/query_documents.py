import os
from database_client import get_dynamodb_client
from database_models import Document

TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "your-dynamodb-table-name")
# In a real scenario, you would have a Global Secondary Index (GSI) for querying by a field value.
# For example, if you want to query by a 'category' field, you would create a GSI on 'category'.
# For this example, we will assume a generic index name if a field_name is provided.
# If no field_name is provided, a scan operation will be performed (not recommended for large tables).

def query_documents(field_name: str = None, field_value: str = None, limit: int = 100):
    dynamodb = get_dynamodb_client()
    documents = []

    try:
        if field_name and field_value:
            # Assuming a GSI exists for the field_name. 
            # Replace 'your-gsi-index-name' with your actual GSI name.
            # For example, if you query by 'category', your GSI name might be 'CategoryIndex'.
            index_name = os.environ.get(f"DYNAMODB_GSI_NAME_{field_name.upper()}", f"{field_name}Index")
            
            response = dynamodb.query(
                TableName=TABLE_NAME,
                IndexName=index_name,
                KeyConditionExpression=f"{field_name} = :val",
                ExpressionAttributeValues={
                    ":val": Document._serialize_value(field_value)
                },
                Limit=limit
            )
        else:
            # If no specific field to query, perform a scan (use with caution on large tables)
            response = dynamodb.scan(
                TableName=TABLE_NAME,
                Limit=limit
            )
        
        for item in response.get("Items", []):
            documents.append(Document.from_item(item).content)

        return {"status": "success", "documents": documents}
    except Exception as e:
        return {"status": "error", "message": str(e)}
