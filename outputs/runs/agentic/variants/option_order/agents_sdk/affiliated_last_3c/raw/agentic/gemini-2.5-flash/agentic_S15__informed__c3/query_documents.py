import boto3
import os
from database_client import get_dynamodb_client

def query_documents(table_name: str, index_name: str, field_name: str, field_value: str) -> list[dict]:
    """
    Queries documents from DynamoDB by a field value or partition-style key
    using a secondary index.
    """
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.query(
            TableName=table_name,
            IndexName=index_name,
            KeyConditionExpression='#fieldName = :fieldValue',
            ExpressionAttributeNames={
                '#fieldName': field_name
            },
            ExpressionAttributeValues={
                ':fieldValue': {'S': field_value}
            }
        )
        items = response.get('Items', [])
        if items:
            print(f"Found {len(items)} documents matching query.")
            from database_models import deserialize_dynamodb_item
            return [deserialize_dynamodb_item(item) for item in items]
        else:
            print(f"No documents found for query on {field_name}={field_value}.")
            return []
    except Exception as e:
        print(f"Error querying documents: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # table_name = os.getenv("DYNAMODB_TABLE_NAME", "my-documents-table")
    # For this example, assume a Global Secondary Index 'CategoryIndex' on attribute 'category'
    # index_name = "CategoryIndex"
    # field_name = "category"
    # field_value = "fiction"
    # documents = query_documents(table_name, index_name, field_name, field_value)
    # if documents:
    #     for doc in documents:
    #         print(doc)
    pass
