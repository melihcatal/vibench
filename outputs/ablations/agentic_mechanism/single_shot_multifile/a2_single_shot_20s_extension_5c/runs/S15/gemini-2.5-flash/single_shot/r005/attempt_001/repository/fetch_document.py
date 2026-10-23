import os
from database_client import get_dynamodb_client
from database_models import Document, TABLE_NAME

def fetch_document(document_id: str) -> Document | None:
    dynamodb = get_dynamodb_client()

    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            'id': {'S': document_id}
        }
    )
    
    item = response.get('Item')
    if not item:
        return None

    # Convert DynamoDB item format to a flat dictionary
    flat_item = {}
    for k, v in item.items():
        if 'S' in v: flat_item[k] = v['S']
        elif 'N' in v: 
            try: flat_item[k] = int(v['N']) 
            except ValueError: flat_item[k] = float(v['N'])
        elif 'BOOL' in v: flat_item[k] = v['BOOL']
        elif 'NULL' in v: flat_item[k] = None
        elif 'M' in v: flat_item[k] = {mk: mv['S'] for mk, mv in v['M'].items()} # Simple map parsing
        # Add more type handling as needed (L, SS, NS, BS, B)

    return Document(**flat_item)
