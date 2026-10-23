import os
from database_client import get_dynamodb_client, get_table_name
from boto3.dynamodb.conditions import Key, Attr

def query_documents(field_name: str, field_value: str, index_name: str = None):
    dynamodb_resource = get_dynamodb_client(is_resource=True)
    table_name = get_table_name()
    table = dynamodb_resource.Table(table_name)

    try:
        if index_name:
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression=Key(field_name).eq(field_value)
            )
        else:
            # Assuming 'id' is the partition key if no index is provided and we're querying directly
            # For querying by non-PK, non-indexed fields, scan would be needed or a GSI.
            # This example assumes either PK query or GSI query.
            # If 'field_name' is the primary key 'id':
            if field_name == 'id':
                response = table.query(
                    KeyConditionExpression=Key(field_name).eq(field_value)
                )
            else:
                # Fallback to scan if no index and not primary key. Not recommended for large tables.
                # For a more efficient query, a GSI is required for non-PK fields.
                response = table.scan(
                    FilterExpression=Attr(field_name).eq(field_value)
                )

        return {"status": "success", "documents": response.get('Items', [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}
