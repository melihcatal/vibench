import os
import json
from typing import List, Dict, Any
from database_client import get_dynamodb_client
from database_models import Document

def query_documents_by_field(table_name: str, index_name: str, field_name: str, field_value: str) -> List[Document]:
    """
    Queries documents by a field value from a managed NoSQL store (DynamoDB).
    Assumes a Global Secondary Index (GSI) exists on the specified field.
    
    Args:
        table_name: The name of the DynamoDB table.
        index_name: The name of the GSI on the field_name.
        field_name: The name of the field to query on (e.g., 'author').
        field_value: The value of the field to match.
        
    Returns:
        A list of Document objects matching the query.
    """
    dynamodb = get_dynamodb_client()
    
    # Construct the KeyConditionExpression dynamically
    key_condition_expression = f"#attr = :val"
    expression_attribute_names = {
        "#attr": field_name
    }
    expression_attribute_values = {
        ":val": {"S": field_value} # Assuming string type for queried field
    }

    response = dynamodb.query(
        TableName=table_name,
        IndexName=index_name,
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )
    
    documents = []
    for item in response.get('Items', []):
        doc = Document.from_item(item)
        if doc:
            documents.append(doc)
            
    return documents

if __name__ == "__main__":
    # Example Usage (requires AWS credentials and DynamoDB table with GSI configured)
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "your-document-table")
    # Assuming a GSI named 'AuthorIndex' on the 'author' field
    index_name = os.getenv("DYNAMODB_AUTHOR_INDEX_NAME", "AuthorIndex") 
    query_field = "author"
    query_value = "Jane Doe"
    
    print(f"Querying documents by {query_field} = '{query_value}'")
    try:
        documents = query_documents_by_field(table_name, index_name, query_field, query_value)
        if documents:
            print(f"Found {len(documents)} document(s):")
            for doc in documents:
                print(json.dumps({"id": doc.id, "data": doc.data}, indent=2))
        else:
            print(f"No documents found for {query_field} = '{query_value}'.")
    except Exception as e:
        print(f"Error querying documents: {e}")
