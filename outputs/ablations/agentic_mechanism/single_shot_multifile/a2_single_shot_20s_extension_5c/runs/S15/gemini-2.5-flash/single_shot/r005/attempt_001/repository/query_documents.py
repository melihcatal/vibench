import os
from typing import List
from database_client import get_dynamodb_client
from database_models import Document, TABLE_NAME

def query_documents_by_field(field_name: str, field_value: str) -> List[Document]:
    dynamodb = get_dynamodb_client()

    # Assuming 'field_name' is a GSI partition key or the primary partition key
    # If it's a GSI, you'd also need IndexName parameter.
    # For this example, let's assume 'field_name' is a primary key or a suitable index key.
    
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression='#fn = :fv',
        ExpressionAttributeNames={
            '#fn': field_name
        },
        ExpressionAttributeValues={
            ':fv': {'S': field_value}
        }
    )
    
    documents = []
    for item in response.get('Items', []):
        flat_item = {}
        for k, v in item.items():
            if 'S' in v: flat_item[k] = v['S']
            elif 'N' in v: 
                try: flat_item[k] = int(v['N']) 
                except ValueError: flat_item[k] = float(v['N'])
            elif 'BOOL' in v: flat_item[k] = v['BOOL']
            elif 'NULL' in v: flat_item[k] = None
            elif 'M' in v: flat_item[k] = {mk: mv['S'] for mk, mv in v['M'].items()} # Simple map parsing
        documents.append(Document(**flat_item))

    return documents
